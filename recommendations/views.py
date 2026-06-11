"""
Views for the Recommendation Engine
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count
from django.core.paginator import Paginator
from django.contrib import messages
import json

from .models import Product, Category, UserRating, UserBehavior, Purchase, UserProfile
from .recommendation_engine import (
    RecommendationService, 
    CollaborativeFiltering,
    ContentBasedFiltering,
    HybridRecommender,
    PopularityBasedRecommender
)


def home(request):
    """Home page with personalized recommendations and trending products"""
    # Get trending products
    trending = RecommendationService.get_trending_products(n=6)

    # Get personalized recommendations
    personalized = RecommendationService.get_personalized_recommendations(
        request.user, n=8
    )

    # Get categories
    categories = Category.objects.filter(parent=None)[:6]

    # Get featured products (highest rated)
    featured = Product.objects.annotate(
        avg_rating=Avg('ratings__rating')
    ).order_by('-avg_rating')[:4]

    context = {
        'trending': trending,
        'personalized': personalized,
        'categories': categories,
        'featured': featured,
    }
    return render(request, 'recommendations/home.html', context)


def product_list(request):
    """Product listing with filtering"""
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'name')

    products = Product.objects.all().select_related('category')

    if category_id:
        products = products.filter(category_id=category_id)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.annotate(avg=Avg('ratings__rating')).order_by('-avg')
    elif sort_by == 'popular':
        products = products.annotate(purchases=Count('purchases')).order_by('-purchases')
    else:
        products = products.order_by('name')

    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    products_page = paginator.get_page(page)

    categories = Category.objects.filter(parent=None)

    context = {
        'products': products_page,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'recommendations/product_list.html', context)


def product_detail(request, product_id):
    """Product detail page with similar products"""
    product = get_object_or_404(Product, id=product_id)

    # Track view behavior
    if request.user.is_authenticated:
        UserBehavior.objects.create(
            user=request.user,
            product=product,
            behavior_type='view',
            metadata={'source': 'product_detail'}
        )
    else:
        session_id = request.session.session_key or request.session._get_or_create_session_key()
        UserBehavior.objects.create(
            session_id=session_id,
            product=product,
            behavior_type='view',
            metadata={'source': 'product_detail'}
        )

    # Get similar products
    similar = RecommendationService.get_similar_products(product_id, n=4)

    # Get user rating if authenticated
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = UserRating.objects.get(user=request.user, product=product)
        except UserRating.DoesNotExist:
            pass

    # Get all ratings
    ratings = UserRating.objects.filter(product=product).select_related('user')

    context = {
        'product': product,
        'similar_products': similar,
        'user_rating': user_rating,
        'ratings': ratings,
    }
    return render(request, 'recommendations/product_detail.html', context)


@login_required
def recommendations_page(request):
    """Dedicated recommendations page"""
    # Collaborative filtering recommendations
    cf = CollaborativeFiltering()
    cf_recs = cf.get_recommendations(request.user.id, n=6)

    # Content-based recommendations
    cb = ContentBasedFiltering()
    cb_recs = cb.get_recommendations(request.user.id, n=6)

    # Hybrid recommendations
    hybrid = HybridRecommender()
    hybrid_recs = hybrid.get_recommendations(request.user.id, n=8)

    # Because you bought (purchase-based)
    recent_purchases = Purchase.objects.filter(
        user=request.user
    ).select_related('product').order_by('-purchase_date')[:3]

    because_you_bought = []
    for purchase in recent_purchases:
        similar = RecommendationService.get_similar_products(purchase.product.id, n=3)
        because_you_bought.append({
            'purchase': purchase,
            'recommendations': similar
        })

    context = {
        'collaborative_recommendations': cf_recs,
        'content_based_recommendations': cb_recs,
        'hybrid_recommendations': hybrid_recs,
        'because_you_bought': because_you_bought,
    }
    return render(request, 'recommendations/recommendations.html', context)


@login_required
@require_POST
def rate_product(request):
    """Rate a product"""
    data = json.loads(request.body)
    product_id = data.get('product_id')
    rating = data.get('rating')
    review = data.get('review', '')

    try:
        product = Product.objects.get(id=product_id)

        # Update or create rating
        user_rating, created = UserRating.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'rating': rating, 'review': review}
        )

        # Update product average rating
        product.update_rating()

        # Track behavior
        UserBehavior.objects.create(
            user=request.user,
            product=product,
            behavior_type='view',
            metadata={'action': 'rated', 'rating': rating}
        )

        return JsonResponse({
            'success': True,
            'message': 'Rating submitted successfully',
            'average_rating': product.average_rating,
            'total_reviews': product.total_reviews,
        })

    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def add_to_cart(request):
    """Add product to cart (simulated)"""
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    try:
        product = Product.objects.get(id=product_id)

        # Track behavior
        UserBehavior.objects.create(
            user=request.user,
            product=product,
            behavior_type='cart_add',
            metadata={'quantity': quantity}
        )

        # Store in session
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart',
            'cart_count': sum(cart.values())
        })

    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})


@login_required
@require_POST
def purchase_product(request):
    """Simulate product purchase"""
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    try:
        product = Product.objects.get(id=product_id)
        total_price = product.price * quantity

        # Create purchase record
        Purchase.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        # Track behavior
        UserBehavior.objects.create(
            user=request.user,
            product=product,
            behavior_type='purchase',
            metadata={'quantity': quantity, 'total_price': str(total_price)}
        )

        # Update user profile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        purchase_history = profile.purchase_history
        purchase_history.append({
            'product_id': product_id,
            'product_name': product.name,
            'category': product.category.name,
            'price': str(product.price),
            'quantity': quantity,
            'date': str(timezone.now())
        })
        profile.purchase_history = purchase_history
        profile.save()

        return JsonResponse({
            'success': True,
            'message': f'Purchased {product.name} successfully!',
        })

    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'recommendations/login.html')


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')

    return render(request, 'recommendations/register.html')


def logout_view(request):
    """User logout"""
    logout(request)
    return redirect('home')


@login_required
def user_profile(request):
    """User profile with recommendations"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Get user's ratings
    ratings = UserRating.objects.filter(user=request.user).select_related('product')

    # Get user's purchases
    purchases = Purchase.objects.filter(user=request.user).select_related('product')

    # Get recommendations
    recommendations = RecommendationService.get_personalized_recommendations(
        request.user, n=6
    )

    context = {
        'profile': profile,
        'ratings': ratings,
        'purchases': purchases,
        'recommendations': recommendations,
    }
    return render(request, 'recommendations/profile.html', context)


def track_behavior(request):
    """Track user behavior via AJAX"""
    if request.method == 'POST':
        data = json.loads(request.body)
        behavior_type = data.get('behavior_type')
        product_id = data.get('product_id')
        metadata = data.get('metadata', {})

        try:
            product = Product.objects.get(id=product_id) if product_id else None

            if request.user.is_authenticated:
                UserBehavior.objects.create(
                    user=request.user,
                    product=product,
                    behavior_type=behavior_type,
                    metadata=metadata
                )
            else:
                session_id = request.session.session_key or request.session._get_or_create_session_key()
                UserBehavior.objects.create(
                    session_id=session_id,
                    product=product,
                    behavior_type=behavior_type,
                    metadata=metadata
                )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


# Admin dashboard views
@login_required
def analytics_dashboard(request):
    """Analytics dashboard for recommendation performance"""
    if not request.user.is_staff:
        return redirect('home')

    # Get statistics
    total_products = Product.objects.count()
    total_users = User.objects.count()
    total_ratings = UserRating.objects.count()
    total_purchases = Purchase.objects.count()
    total_behaviors = UserBehavior.objects.count()

    # Top rated products
    top_rated = Product.objects.annotate(
        avg_rating=Avg('ratings__rating'),
        rating_count=Count('ratings')
    ).filter(rating_count__gt=0).order_by('-avg_rating')[:10]

    # Most purchased products
    most_purchased = Product.objects.annotate(
        purchase_count=Count('purchases')
    ).filter(purchase_count__gt=0).order_by('-purchase_count')[:10]

    # Recent activity
    recent_behaviors = UserBehavior.objects.select_related('user', 'product').order_by('-timestamp')[:20]

    # Behavior distribution
    behavior_dist = UserBehavior.objects.values('behavior_type').annotate(
        count=Count('id')
    ).order_by('-count')

    context = {
        'total_products': total_products,
        'total_users': total_users,
        'total_ratings': total_ratings,
        'total_purchases': total_purchases,
        'total_behaviors': total_behaviors,
        'top_rated': top_rated,
        'most_purchased': most_purchased,
        'recent_behaviors': recent_behaviors,
        'behavior_distribution': behavior_dist,
    }
    return render(request, 'recommendations/analytics.html', context)
