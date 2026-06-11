"""
User Behavior Tracking Middleware
"""
from .models import UserBehavior, Product


class UserBehaviorMiddleware:
    """Middleware to track user browsing behavior"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Track page views for product pages
        if request.path.startswith('/products/') and request.path != '/products/':
            try:
                product_id = int(request.path.split('/')[-2])
                product = Product.objects.get(id=product_id)

                if request.user.is_authenticated:
                    UserBehavior.objects.create(
                        user=request.user,
                        product=product,
                        behavior_type='view',
                        metadata={'source': 'middleware', 'path': request.path}
                    )
                else:
                    session_id = request.session.session_key
                    if session_id:
                        UserBehavior.objects.create(
                            session_id=session_id,
                            product=product,
                            behavior_type='view',
                            metadata={'source': 'middleware', 'path': request.path}
                        )
            except (ValueError, Product.DoesNotExist):
                pass

        return response
