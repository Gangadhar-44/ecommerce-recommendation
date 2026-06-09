"""
Admin configuration for Recommendation Engine
"""
from django.contrib import admin
from .models import Category, Product, UserProfile, UserRating, UserBehavior, Purchase, RecommendationCache


# Register all models with the admin site
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(UserRating)
admin.site.register(UserBehavior)
admin.site.register(Purchase)
admin.site.register(RecommendationCache)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'description']
    list_filter = ['parent']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'average_rating', 'stock_quantity', 'created_at']
    list_filter = ['category', 'brand', 'created_at']
    search_fields = ['name', 'description', 'brand']
    readonly_fields = ['average_rating', 'total_reviews']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferences_summary']
    search_fields = ['user__username']

    def preferences_summary(self, obj):
        return f"{len(obj.preferences)} preferences, {len(obj.purchase_history)} purchases"


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'product__name']


@admin.register(UserBehavior)
class UserBehaviorAdmin(admin.ModelAdmin):
    list_display = ['behavior_type', 'user', 'product', 'timestamp']
    list_filter = ['behavior_type', 'timestamp']
    search_fields = ['user__username', 'product__name']
    date_hierarchy = 'timestamp'


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'total_price', 'purchase_date']
    list_filter = ['purchase_date']
    search_fields = ['user__username', 'product__name']
    date_hierarchy = 'purchase_date'


@admin.register(RecommendationCache)
class RecommendationCacheAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'score', 'algorithm', 'created_at']
    list_filter = ['algorithm', 'created_at']
