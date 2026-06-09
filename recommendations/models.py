"""
Models for the Recommendation Engine
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=100)
    image_url = models.CharField(max_length=500, default='/static/recommendations/images/placeholder.jpg')
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    stock_quantity = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def update_rating(self):
        ratings = UserRating.objects.filter(product=self)
        if ratings.exists():
            self.average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
            self.total_reviews = ratings.count()
            self.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferences = models.JSONField(default=dict, blank=True)
    browsing_history = models.JSONField(default=list, blank=True)
    purchase_history = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} rated {self.product.name}: {self.rating}"


class UserBehavior(models.Model):
    BEHAVIOR_TYPES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('cart_add', 'Add to Cart'),
        ('cart_remove', 'Remove from Cart'),
        ('purchase', 'Purchase'),
        ('wishlist', 'Add to Wishlist'),
        ('search', 'Search'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behaviors', null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='behaviors', null=True, blank=True)
    behavior_type = models.CharField(max_length=20, choices=BEHAVIOR_TYPES)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.behavior_type} by {self.user or self.session_id} on {self.product}"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.product.name}"


class RecommendationCache(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_cache')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = models.FloatField()
    algorithm = models.CharField(max_length=50)  # 'collaborative', 'content_based', 'hybrid'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']
