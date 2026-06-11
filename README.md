# ShopSmart - AI-Powered E-Commerce Recommendation Engine

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0-green)](https://djangoproject.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange)](https://scikit-learn.org)

A comprehensive Django-based e-commerce platform with an intelligent recommendation system powered by **Collaborative Filtering** and **Content-Based Filtering** algorithms.

## Features

- **Collaborative Filtering**: User-based similarity using cosine similarity
- **Content-Based Filtering**: TF-IDF vectorization of product features
- **Hybrid Engine**: Weighted combination for optimal recommendations
- **Real-time Behavior Tracking**: Views, clicks, cart additions, purchases
- **Admin Dashboard**: Analytics and management interface
- **Responsive Design**: Modern UI with Bootstrap 5

## Screenshots

| Home Page | Recommendations | Admin Dashboard |
|-----------|----------------|-----------------|
| Personalized products | ML algorithms in action | Analytics & insights |

## Tech Stack

- **Backend**: Django 5.0, Python 3.11
- **ML**: scikit-learn, NumPy, Pandas
- **Database**: PostgreSQL / SQLite
- **Frontend**: Bootstrap 5, JavaScript
- **Deployment**: Docker, Heroku, AWS ready

## Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/ecommerce-recommendation.git
cd ecommerce-recommendation

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Demo Accounts

| Username | Password |
|----------|----------|
| demo_user1 | demo123 |
| demo_user2 | demo123 |
| demo_user3 | demo123 |

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guides:
- Docker
- Heroku
- AWS EC2
- PythonAnywhere
- VPS

## Project Structure

```
ecommerce_recommendation/
├── ecommerce_recommendation/    # Django settings
├── recommendations/             # Main app
│   ├── models.py                 # Database models
│   ├── views.py                  # Views
│   ├── recommendation_engine.py  # ML algorithms
│   ├── templates/                # HTML templates
│   └── static/                   # CSS, JS, images
├── manage.py
├── requirements.txt
└── README.md
```

## License

MIT License
