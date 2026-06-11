# Generated migration for demo data
from django.db import migrations


def create_demo_data(apps, schema_editor):
    Category = apps.get_model('recommendations', 'Category')
    Product = apps.get_model('recommendations', 'Product')
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('recommendations', 'UserProfile')
    UserRating = apps.get_model('recommendations', 'UserRating')
    Purchase = apps.get_model('recommendations', 'Purchase')
    UserBehavior = apps.get_model('recommendations', 'UserBehavior')

    # Create categories
    electronics = Category.objects.create(
        name='Electronics',
        description='Electronic devices and gadgets'
    )

    phones = Category.objects.create(
        name='Smartphones',
        description='Mobile phones and accessories',
        parent=electronics
    )

    laptops = Category.objects.create(
        name='Laptops',
        description='Notebook computers and accessories',
        parent=electronics
    )

    audio = Category.objects.create(
        name='Audio',
        description='Headphones, speakers, and audio equipment',
        parent=electronics
    )

    cameras = Category.objects.create(
        name='Cameras',
        description='Digital cameras and photography equipment',
        parent=electronics
    )

    gaming = Category.objects.create(
        name='Gaming',
        description='Gaming consoles and accessories',
        parent=electronics
    )

    tablets = Category.objects.create(
        name='Tablets',
        description='Tablet computers and e-readers',
        parent=electronics
    )

    wearables = Category.objects.create(
        name='Wearables',
        description='Smartwatches and fitness trackers',
        parent=electronics
    )

    fashion = Category.objects.create(
        name='Fashion',
        description='Clothing, shoes, and accessories'
    )

    footwear = Category.objects.create(
        name='Footwear',
        description='Shoes and footwear',
        parent=fashion
    )

    home = Category.objects.create(
        name='Home & Kitchen',
        description='Home appliances and kitchen equipment'
    )

    # Create products
    products_data = [
        {
            'name': 'iPhone 15 Pro',
            'description': 'Latest flagship smartphone with A17 Pro chip, titanium design, and advanced camera system. Features 48MP main camera, 5x telephoto zoom, and all-day battery life.',
            'price': 999.99,
            'category': phones,
            'brand': 'Apple',
            'tags': 'smartphone, ios, flagship, camera, 5g, premium',
            'stock_quantity': 50,
            'image_url': '/static/recommendations/image_urls/8_iPhone_vs_Samsung_The_ultimate_head.png'
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'description': 'Premium Android smartphone with S Pen, 200MP camera, and AI-powered features. Features 6.8-inch AMOLED display and Snapdragon 8 Gen 3 processor.',
            'price': 1299.99,
            'category': phones,
            'brand': 'Samsung',
            'tags': 'smartphone, android, flagship, camera, s-pen, ai',
            'stock_quantity': 45,
            'image_url': '/static/recommendations/image_urls/2_3_919_Iphone_Samsung_Phones_Royalty.png'
        },
        {
            'name': 'MacBook Pro 16"',
            'description': 'Professional laptop with M3 Pro chip, 16-inch Liquid Retina XDR display, and up to 22 hours battery life. Perfect for creative professionals and developers.',
            'price': 2499.99,
            'category': laptops,
            'brand': 'Apple',
            'tags': 'laptop, macbook, professional, creative, m3, retina',
            'stock_quantity': 30,
            'image_url': '/static/recommendations/image_urls/3_Browse_thousands_of_E_Commerce_Laptop.png'
        },
        {
            'name': 'Dell XPS 15',
            'description': 'Premium Windows laptop with Intel Core i9, NVIDIA RTX 4070, and 15.6-inch OLED display. Ideal for gaming and content creation.',
            'price': 1899.99,
            'category': laptops,
            'brand': 'Dell',
            'tags': 'laptop, windows, gaming, oled, rtx, premium',
            'stock_quantity': 25,
            'image_url': '/static/recommendations/image_urls/6_How_to_bring_the_same_B2C_customer.png'
        },
        {
            'name': 'Sony WH-1000XM5',
            'description': 'Industry-leading noise canceling headphones with 30-hour battery life, crystal clear hands-free calling, and premium comfort for all-day wear.',
            'price': 399.99,
            'category': audio,
            'brand': 'Sony',
            'tags': 'headphones, noise-canceling, wireless, bluetooth, premium, audio',
            'stock_quantity': 60,
            'image_url': '/static/recommendations/image_urls/1_Audio_Technica_ATH_S300BT_Wireless.png'
        },
        {
            'name': 'Audio-Technica ATH-S300BT',
            'description': 'Wireless over-ear headphones with high-quality sound reproduction, comfortable design, and long battery life. Perfect for audiophiles.',
            'price': 299.99,
            'category': audio,
            'brand': 'Audio-Technica',
            'tags': 'headphones, wireless, over-ear, audiophile, bluetooth, audio',
            'stock_quantity': 40,
            'image_url': '/static/recommendations/image_urls/1_Audio_Technica_ATH_S300BT_Wireless.png'
        },
        {
            'name': 'Canon EOS R5',
            'description': 'Professional mirrorless camera with 45MP full-frame sensor, 8K video recording, and advanced autofocus system. Perfect for professional photographers.',
            'price': 3899.99,
            'category': cameras,
            'brand': 'Canon',
            'tags': 'camera, mirrorless, professional, 8k, full-frame, photography',
            'stock_quantity': 15,
            'image_url': '/static/recommendations/image_urls/3_The_9_Best_mirrorless_cameras_in.png'
        },
        {
            'name': 'Nikon Z8',
            'description': 'High-performance mirrorless camera with 45.7MP sensor, 8K video, and robust build quality. Features advanced subject detection and tracking.',
            'price': 3499.99,
            'category': cameras,
            'brand': 'Nikon',
            'tags': 'camera, mirrorless, professional, 8k, nikon, photography',
            'stock_quantity': 20,
            'image_url': '/static/recommendations/image_urls/7_Mirrorless_Camera_High_Quality_Dslr.png'
        },
        {
            'name': 'PlayStation 5',
            'description': 'Next-gen gaming console with ultra-high speed SSD, ray tracing, 4K gaming, and haptic feedback DualSense controller. Includes exclusive game library.',
            'price': 499.99,
            'category': gaming,
            'brand': 'Sony',
            'tags': 'gaming, console, playstation, 4k, ray-tracing, ssd',
            'stock_quantity': 35,
            'image_url': '/static/recommendations/image_urls/4_Playstation_or_Xbox_Which_game_console.png'
        },
        {
            'name': 'Xbox Series X',
            'description': 'Most powerful Xbox console with 12 teraflops GPU, 1TB SSD, and 4K gaming at 120fps. Includes Game Pass integration for hundreds of games.',
            'price': 499.99,
            'category': gaming,
            'brand': 'Microsoft',
            'tags': 'gaming, console, xbox, 4k, 120fps, game-pass',
            'stock_quantity': 30,
            'image_url': '/static/recommendations/image_urls/5_New_Xbox_Xbox_One_X_Playstation_PlayStation.png'
        },
        {
            'name': 'iPad Pro 12.9"',
            'description': 'Professional tablet with M2 chip, Liquid Retina XDR display, and Apple Pencil support. Perfect for creative work and productivity.',
            'price': 1099.99,
            'category': tablets,
            'brand': 'Apple',
            'tags': 'tablet, ipad, professional, m2, pencil, creative',
            'stock_quantity': 40,
            'image_url': '/static/recommendations/image_urls/6_Buy_iPad_Apple_IN_.png'
        },
        {
            'name': 'iPad Air',
            'description': 'Versatile tablet with M1 chip, 10.9-inch display, and vibrant colors. Great for students, professionals, and everyday use.',
            'price': 599.99,
            'category': tablets,
            'brand': 'Apple',
            'tags': 'tablet, ipad, versatile, m1, student, colorful',
            'stock_quantity': 55,
            'image_url': '/static/recommendations/image_urls/10_Apple_iPad_Apple_.png'
        },
        {
            'name': 'Apple Watch Ultra 2',
            'description': 'Rugged smartwatch with titanium case, advanced health sensors, and 36-hour battery life. Features depth gauge and water temperature sensor.',
            'price': 799.99,
            'category': wearables,
            'brand': 'Apple',
            'tags': 'smartwatch, fitness, health, titanium, rugged, gps',
            'stock_quantity': 25,
            'image_url': '/static/recommendations/image_urls/9_The_3_Best_Fitness_Trackers_of_2026.png'
        },
        {
            'name': 'Samsung Galaxy Watch 6',
            'description': 'Advanced smartwatch with health monitoring, sleep tracking, and body composition analysis. Features rotating bezel and vibrant AMOLED display.',
            'price': 299.99,
            'category': wearables,
            'brand': 'Samsung',
            'tags': 'smartwatch, fitness, health, android, sleep, body-composition',
            'stock_quantity': 45,
            'image_url': '/static/recommendations/image_urls/9_The_3_Best_Fitness_Trackers_of_2026.png'
        },
        {
            'name': 'Nike Air Max 90',
            'description': 'Iconic running shoes with visible Air cushioning, premium materials, and timeless design. Available in multiple colorways for everyday style.',
            'price': 129.99,
            'category': footwear,
            'brand': 'Nike',
            'tags': 'shoes, running, sneakers, air-max, casual, sport',
            'stock_quantity': 80,
            'image_url': '/static/recommendations/image_urls/4_Dots_Background_Blue_Shoes_Photo.png'
        },
        {
            'name': 'Adidas Ultraboost 23',
            'description': 'Premium running shoes with Boost midsole technology, Primeknit upper, and Continental rubber outsole. Ultimate comfort and energy return.',
            'price': 189.99,
            'category': footwear,
            'brand': 'Adidas',
            'tags': 'shoes, running, sneakers, boost, comfort, performance',
            'stock_quantity': 70,
            'image_url': '/static/recommendations/image_urls/1_Men_s_Leather_Shoes_Fashion_New_Arrival.png'
        },
        {
            'name': 'LG Smart Refrigerator',
            'description': 'Energy-efficient smart refrigerator with InstaView door, WiFi connectivity, and advanced cooling technology. Features voice control integration.',
            'price': 2499.99,
            'category': home,
            'brand': 'LG',
            'tags': 'refrigerator, smart, kitchen, energy-efficient, wifi, appliance',
            'stock_quantity': 10,
            'image_url': '/static/recommendations/image_urls/5_Zoovu_for_Home_Appliances_Ecommerce.png'
        },
        {
            'name': 'Dyson V15 Detect',
            'description': 'Cordless vacuum with laser dust detection, intelligent suction optimization, and up to 60 minutes runtime. Perfect for all floor types.',
            'price': 749.99,
            'category': home,
            'brand': 'Dyson',
            'tags': 'vacuum, cordless, smart, cleaning, laser, home',
            'stock_quantity': 20,
            'image_url': '/static/recommendations/image_urls/5_Zoovu_for_Home_Appliances_Ecommerce.png'
        },
    ]

    created_products = []
    for data in products_data:
        product = Product.objects.create(**data)
        created_products.append(product)

    # Create demo users
    users_data = [
        {'username': 'demo_user1', 'email': 'demo1@example.com', 'password': 'demo123'},
        {'username': 'demo_user2', 'email': 'demo2@example.com', 'password': 'demo123'},
        {'username': 'demo_user3', 'email': 'demo3@example.com', 'password': 'demo123'},
        {'username': 'demo_user4', 'email': 'demo4@example.com', 'password': 'demo123'},
        {'username': 'demo_user5', 'email': 'demo5@example.com', 'password': 'demo123'},
    ]

    created_users = []
    for data in users_data:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        UserProfile.objects.create(user=user)
        created_users.append(user)

    # Create ratings to build collaborative filtering data
    import random
    random.seed(42)

    for user in created_users:
        # Each user rates 8-12 random products
        num_ratings = random.randint(8, 12)
        rated_products = random.sample(created_products, num_ratings)

        for product in rated_products:
            rating = random.randint(3, 5)
            UserRating.objects.create(
                user=user,
                product=product,
                rating=rating,
                review=f'Great product! Really satisfied with the {product.name}. Would recommend to others.'
            )

    # Create some purchases
    for user in created_users:
        num_purchases = random.randint(3, 6)
        purchased_products = random.sample(created_products, num_purchases)

        for product in purchased_products:
            Purchase.objects.create(
                user=user,
                product=product,
                quantity=random.randint(1, 3),
                total_price=product.price * random.randint(1, 3)
            )

    # Create browsing behaviors
    behavior_types = ['view', 'click', 'cart_add', 'search']
    for user in created_users:
        for _ in range(random.randint(20, 40)):
            product = random.choice(created_products)
            behavior = random.choice(behavior_types)
            UserBehavior.objects.create(
                user=user,
                product=product,
                behavior_type=behavior,
                metadata={'page': 'product_detail'}
            )


def delete_demo_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('recommendations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_demo_data, delete_demo_data),
    ]
