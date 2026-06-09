"""
Recommendation Engine Core
Implements Collaborative Filtering and Content-Based Filtering algorithms
"""
import numpy as np
from collections import defaultdict
from django.db.models import Avg, Count, Q
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from .models import Product, UserRating, UserBehavior, Purchase, UserProfile


class CollaborativeFiltering:
    """
    User-Based Collaborative Filtering using cosine similarity
    """
    def __init__(self, k_neighbors=5, min_ratings=2):
        self.k_neighbors = k_neighbors
        self.min_ratings = min_ratings
        self.user_item_matrix = None
        self.user_similarity_matrix = None
        self.users = []
        self.products = []

    def build_user_item_matrix(self):
        """Build user-item rating matrix"""
        ratings = UserRating.objects.all().select_related('user', 'product')

        if not ratings.exists():
            return None

        # Create mappings
        users = list(set(r.user_id for r in ratings))
        products = list(set(r.product_id for r in ratings))

        self.users = users
        self.products = products

        user_idx = {u: i for i, u in enumerate(users)}
        product_idx = {p: i for i, p in enumerate(products)}

        # Build matrix
        matrix = np.zeros((len(users), len(products)))
        for rating in ratings:
            u_idx = user_idx[rating.user_id]
            p_idx = product_idx[rating.product_id]
            matrix[u_idx][p_idx] = rating.rating

        self.user_item_matrix = matrix
        return matrix, user_idx, product_idx

    def compute_user_similarity(self):
        """Compute cosine similarity between users"""
        if self.user_item_matrix is None:
            self.build_user_item_matrix()

        if self.user_item_matrix is None or len(self.users) < 2:
            return None

        # Normalize by subtracting user mean
        normalized = self.user_item_matrix.copy()
        user_means = np.mean(normalized, axis=1, keepdims=True)
        user_means[user_means == 0] = 1  # Avoid division by zero
        normalized = normalized - user_means

        # Compute cosine similarity
        similarity = cosine_similarity(normalized)
        self.user_similarity_matrix = similarity
        return similarity

    def get_similar_users(self, user_id, n=5):
        """Get top N similar users"""
        if self.user_similarity_matrix is None:
            self.compute_user_similarity()

        if self.user_similarity_matrix is None:
            return []

        try:
            user_idx = self.users.index(user_id)
        except ValueError:
            return []

        similarities = self.user_similarity_matrix[user_idx]
        # Exclude self (similarity = 1.0)
        similar_indices = np.argsort(similarities)[::-1][1:n+1]

        similar_users = []
        for idx in similar_indices:
            if similarities[idx] > 0:
                similar_users.append({
                    'user_id': self.users[idx],
                    'similarity': float(similarities[idx])
                })

        return similar_users

    def predict_ratings(self, user_id):
        """Predict ratings for all products for a given user"""
        if self.user_similarity_matrix is None:
            self.compute_user_similarity()

        if self.user_item_matrix is None:
            return {}

        try:
            user_idx = self.users.index(user_id)
        except ValueError:
            return {}

        user_ratings = self.user_item_matrix[user_idx]
        similarities = self.user_similarity_matrix[user_idx]

        predictions = {}
        for p_idx in range(len(self.products)):
            if user_ratings[p_idx] == 0:  # Only predict for unrated items
                # Weighted average of similar users' ratings
                weighted_sum = 0
                similarity_sum = 0

                for u_idx in range(len(self.users)):
                    if u_idx != user_idx and self.user_item_matrix[u_idx][p_idx] > 0:
                        sim = similarities[u_idx]
                        if sim > 0:
                            weighted_sum += sim * self.user_item_matrix[u_idx][p_idx]
                            similarity_sum += sim

                if similarity_sum > 0:
                    predictions[self.products[p_idx]] = weighted_sum / similarity_sum

        return predictions

    def get_recommendations(self, user_id, n=10):
        """Get top N product recommendations"""
        predictions = self.predict_ratings(user_id)

        if not predictions:
            return []

        # Sort by predicted rating
        sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)

        recommendations = []
        for product_id, score in sorted_predictions[:n]:
            try:
                product = Product.objects.get(id=product_id)
                recommendations.append({
                    'product': product,
                    'score': round(score, 2),
                    'algorithm': 'collaborative_filtering'
                })
            except Product.DoesNotExist:
                continue

        return recommendations


class ContentBasedFiltering:
    """
    Content-Based Filtering using TF-IDF and product features
    """
    def __init__(self):
        self.tfidf_matrix = None
        self.vectorizer = None
        self.products = []

    def build_product_features(self):
        """Build feature vectors for all products"""
        products = Product.objects.all().select_related('category')

        if not products.exists():
            return None

        self.products = list(products)

        # Create text features combining name, description, category, brand, tags
        product_texts = []
        for product in self.products:
            text = f"{product.name} {product.description} {product.category.name} {product.brand} {product.tags}"
            product_texts.append(text)

        # TF-IDF vectorization
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(product_texts)

        return self.tfidf_matrix

    def get_user_profile_vector(self, user_id):
        """Build user profile vector based on their interactions"""
        # Get user's rated, viewed, and purchased products
        rated_products = UserRating.objects.filter(user_id=user_id).select_related('product')
        viewed_products = UserBehavior.objects.filter(
            user_id=user_id, 
            behavior_type='view'
        ).select_related('product')
        purchased_products = Purchase.objects.filter(
            user_id=user_id
        ).select_related('product')

        # Collect product IDs with weights
        product_weights = defaultdict(float)

        for rating in rated_products:
            product_weights[rating.product_id] += rating.rating * 2

        for view in viewed_products:
            product_weights[view.product_id] += 0.5

        for purchase in purchased_products:
            product_weights[purchase.product_id] += 3.0

        if not product_weights:
            return None

        # Build user profile by averaging weighted product vectors
        if self.tfidf_matrix is None:
            self.build_product_features()

        if self.tfidf_matrix is None:
            return None

        product_id_to_idx = {p.id: i for i, p in enumerate(self.products)}

        user_vector = np.zeros(self.tfidf_matrix.shape[1])
        total_weight = 0

        for pid, weight in product_weights.items():
            if pid in product_id_to_idx:
                idx = product_id_to_idx[pid]
                user_vector += weight * self.tfidf_matrix[idx].toarray().flatten()
                total_weight += weight

        if total_weight > 0:
            user_vector /= total_weight

        return user_vector

    def get_recommendations(self, user_id, n=10):
        """Get content-based recommendations"""
        user_vector = self.get_user_profile_vector(user_id)

        if user_vector is None or self.tfidf_matrix is None:
            return []

        # Compute similarity between user profile and all products
        similarities = cosine_similarity(
            user_vector.reshape(1, -1),
            self.tfidf_matrix
        ).flatten()

        # Get products the user has already interacted with
        interacted = set()
        interacted.update(UserRating.objects.filter(user_id=user_id).values_list('product_id', flat=True))
        interacted.update(Purchase.objects.filter(user_id=user_id).values_list('product_id', flat=True))

        # Filter out already interacted products and sort by similarity
        recommendations = []
        for i, score in enumerate(similarities):
            product = self.products[i]
            if product.id not in interacted and score > 0.01:
                recommendations.append({
                    'product': product,
                    'score': round(float(score), 4),
                    'algorithm': 'content_based'
                })

        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:n]


class HybridRecommender:
    """
    Hybrid recommendation combining Collaborative and Content-Based filtering
    """
    def __init__(self, cf_weight=0.6, cb_weight=0.4):
        self.cf_weight = cf_weight
        self.cb_weight = cb_weight
        self.cf_engine = CollaborativeFiltering()
        self.cb_engine = ContentBasedFiltering()

    def get_recommendations(self, user_id, n=10):
        """Get hybrid recommendations"""
        # Get recommendations from both engines
        cf_recs = self.cf_engine.get_recommendations(user_id, n=n*2)
        cb_recs = self.cb_engine.get_recommendations(user_id, n=n*2)

        # Normalize scores
        cf_scores = {r['product'].id: r['score'] for r in cf_recs}
        cb_scores = {r['product'].id: r['score'] for r in cb_recs}

        # Normalize to 0-1 range
        if cf_scores:
            cf_max = max(cf_scores.values())
            cf_min = min(cf_scores.values())
            if cf_max > cf_min:
                cf_scores = {k: (v - cf_min) / (cf_max - cf_min) for k, v in cf_scores.items()}

        if cb_scores:
            cb_max = max(cb_scores.values())
            cb_min = min(cb_scores.values())
            if cb_max > cb_min:
                cb_scores = {k: (v - cb_min) / (cb_max - cb_min) for k, v in cb_scores.items()}

        # Combine scores
        all_product_ids = set(cf_scores.keys()) | set(cb_scores.keys())
        hybrid_scores = {}

        for pid in all_product_ids:
            cf_score = cf_scores.get(pid, 0)
            cb_score = cb_scores.get(pid, 0)

            # Weighted combination
            hybrid_scores[pid] = (self.cf_weight * cf_score + self.cb_weight * cb_score)

        # Sort and get top N
        sorted_scores = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)

        recommendations = []
        for pid, score in sorted_scores[:n]:
            try:
                product = Product.objects.get(id=pid)
                recommendations.append({
                    'product': product,
                    'score': round(score, 4),
                    'algorithm': 'hybrid'
                })
            except Product.DoesNotExist:
                continue

        return recommendations


class PopularityBasedRecommender:
    """
    Fallback recommender based on popularity for cold start users
    """
    @staticmethod
    def get_recommendations(n=10):
        """Get most popular products"""
        popular_products = Product.objects.annotate(
            purchase_count=Count('purchases'),
            avg_rating=Avg('ratings__rating')
        ).order_by('-purchase_count', '-avg_rating')[:n]

        recommendations = []
        for product in popular_products:
            score = (product.purchase_count or 0) * 0.5 + (product.average_rating or 0) * 0.5
            recommendations.append({
                'product': product,
                'score': round(score, 2),
                'algorithm': 'popularity'
            })

        return recommendations


class RecommendationService:
    """
    Main service class that orchestrates all recommendation algorithms
    """
    @staticmethod
    def get_personalized_recommendations(user, n=10):
        """Get best recommendations for a user based on their history"""
        if not user or not user.is_authenticated:
            # Return popular items for anonymous users
            return PopularityBasedRecommender.get_recommendations(n)

        # Check if user has enough interaction history
        rating_count = UserRating.objects.filter(user=user).count()
        purchase_count = Purchase.objects.filter(user=user).count()
        view_count = UserBehavior.objects.filter(user=user, behavior_type='view').count()

        total_interactions = rating_count + purchase_count + view_count

        if total_interactions < 3:
            # Cold start: return popular + trending
            return PopularityBasedRecommender.get_recommendations(n)

        # Use hybrid recommender for users with history
        hybrid = HybridRecommender()
        recommendations = hybrid.get_recommendations(user.id, n)

        if not recommendations:
            return PopularityBasedRecommender.get_recommendations(n)

        return recommendations

    @staticmethod
    def get_similar_products(product_id, n=5):
        """Get products similar to a given product"""
        try:
            target_product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return []

        cb = ContentBasedFiltering()
        cb.build_product_features()

        if cb.tfidf_matrix is None:
            return []

        # Find index of target product
        product_id_to_idx = {p.id: i for i, p in enumerate(cb.products)}

        if target_product.id not in product_id_to_idx:
            return []

        target_idx = product_id_to_idx[target_product.id]
        target_vector = cb.tfidf_matrix[target_idx]

        # Compute similarity with all products
        similarities = cosine_similarity(target_vector, cb.tfidf_matrix).flatten()

        similar_products = []
        for i, score in enumerate(similarities):
            product = cb.products[i]
            if product.id != target_product.id and score > 0.05:
                similar_products.append({
                    'product': product,
                    'score': round(float(score), 4),
                    'algorithm': 'content_similarity'
                })

        similar_products.sort(key=lambda x: x['score'], reverse=True)
        return similar_products[:n]

    @staticmethod
    def get_trending_products(n=10):
        """Get currently trending products based on recent activity"""
        from django.utils import timezone
        from datetime import timedelta

        recent_date = timezone.now() - timedelta(days=7)

        trending = Product.objects.filter(
            behaviors__timestamp__gte=recent_date
        ).annotate(
            recent_views=Count('behaviors', filter=Q(behaviors__behavior_type='view')),
            recent_purchases=Count('purchases', filter=Q(purchases__purchase_date__gte=recent_date))
        ).order_by('-recent_views', '-recent_purchases')[:n]

        recommendations = []
        for product in trending:
            score = (product.recent_views or 0) + (product.recent_purchases or 0) * 3
            recommendations.append({
                'product': product,
                'score': score,
                'algorithm': 'trending'
            })

        return recommendations
