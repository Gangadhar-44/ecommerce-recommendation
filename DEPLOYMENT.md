# Deployment Guide for ShopSmart Recommendation Engine

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS Deployment](#aws-deployment)
5. [PythonAnywhere Deployment](#pythonanywhere-deployment)
6. [VPS/Server Deployment](#vps-server-deployment)

---

## Local Development

```bash
# 1. Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Collect static files
python manage.py collectstatic

# 6. Run server
python manage.py runserver
```

---

## Docker Deployment (Recommended)

### Prerequisites
- Docker Desktop installed
- Docker Compose installed

### Steps

```bash
# 1. Build and start containers
docker-compose up --build

# 2. Run migrations in container
docker-compose exec web python manage.py migrate

# 3. Create superuser
docker-compose exec web python manage.py createsuperuser

# 4. Access the app
# http://localhost:80
```

### Stop Docker
```bash
docker-compose down
```

---

## Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Git repository initialized

### Steps

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create your-app-name

# 3. Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# 4. Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# 5. Deploy
git add .
git commit -m "Initial deployment"
git push heroku main

# 6. Run migrations
heroku run python manage.py migrate

# 7. Create superuser
heroku run python manage.py createsuperuser

# 8. Open app
heroku open
```

---

## AWS Deployment (EC2)

### Prerequisites
- AWS account
- EC2 instance running Ubuntu 22.04

### Steps

```bash
# 1. SSH into your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Update system
sudo apt update && sudo apt upgrade -y

# 3. Install Python and PostgreSQL
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx -y

# 4. Clone your repository
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# 5. Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt

# 7. Setup PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE ecommerce_db;"
sudo -u postgres psql -c "CREATE USER dbuser WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO dbuser;"

# 8. Configure environment
cp .env.example .env
# Edit .env with your settings

# 9. Run migrations
python manage.py migrate

# 10. Collect static files
python manage.py collectstatic

# 11. Create superuser
python manage.py createsuperuser

# 12. Configure Gunicorn
sudo nano /etc/systemd/system/gunicorn.service
```

**gunicorn.service content:**
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/your-repo
ExecStart=/home/ubuntu/your-repo/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/your-repo/app.sock ecommerce_recommendation.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# 13. Configure Nginx
sudo nano /etc/nginx/sites-available/your-app
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/your-repo;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/your-repo/app.sock;
    }
}
```

```bash
# 14. Enable site
sudo ln -s /etc/nginx/sites-available/your-app /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# 15. Start Gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

## PythonAnywhere Deployment

### Steps

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Open a Bash console
3. Upload your code or clone from GitHub
4. Create virtual environment
5. Install requirements
6. Configure WSGI file
7. Set static files path
8. Reload web app

**WSGI file configuration:**
```python
import os
import sys

path = '/home/yourusername/ecommerce_recommendation'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_recommendation.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## VPS/Server Deployment

### Using the Setup Script

```bash
# 1. Upload project to server
scp -r ecommerce_recommendation user@server:/var/www/

# 2. SSH into server
ssh user@server

# 3. Navigate to project
cd /var/www/ecommerce_recommendation

# 4. Run setup
chmod +x setup.sh
./setup.sh

# 5. Configure production settings
cp .env.example .env
nano .env

# 6. Run production server
python manage.py runserver 0.0.0.0:8000
```

---

## Environment Variables

Create a `.env` file in production:

```bash
SECRET_KEY=your-secure-secret-key
DEBUG=false
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=secure-password
DB_HOST=localhost
DB_PORT=5432
```

---

## Post-Deployment Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup PostgreSQL database
- [ ] Collect static files
- [ ] Create superuser
- [ ] Configure SSL/HTTPS
- [ ] Setup backup strategy
- [ ] Configure monitoring
- [ ] Test all features

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Static files not loading | Run `collectstatic` and configure web server |
| Database connection error | Check DB credentials and ensure PostgreSQL is running |
| 500 errors | Check logs: `tail -f django.log` |
| Port already in use | Change port: `python manage.py runserver 8080` |
| Permission denied | Check file permissions: `chmod 755` |

---

## Support

For issues or questions, refer to the README.md or create an issue in the repository.
