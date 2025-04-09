# Simplify Tasks

## Overview
Simplify Tasks is a streamlined web platform designed to help you manage tasks, projects, teams, and users with ease. 
Whether you're organizing personal to-dos or coordinating team efforts, Simplify Tasks keeps everything clear, connected, and under control.

## Features
- Django 5.1.5
- User authentication
- Django jazzmin admin panel
- Separated functionality based on user roles.
- Static/Media files handling by AWS S3
- External Postgres DB

## Live Demo

### 🔗 Link
- [Visit Website](https://your-project-demo-link.com)

#### 👤 Admin
- **username:** admin  
- **password:** admin

#### 👤 User
- **username:** user  
- **password:** testuser12345

_If you can't connect, wait around 2-3 minutes, website needs to start up_

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.9+
- PostgreSQL (or SQLite for development)
- Virtual environment tool (e.g., `venv` or `virtualenv`)

### Setup

#### Clone the repository
```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

#### Configure .env file
```.env
# DB
POSTGRES_DB=<DB>
POSTGRES_DB_PORT=5432
POSTGRES_USER=<USER>
POSTGRES_PASSWORD=<PASSWORD>
POSTGRES_HOST=<HOST>

# Django
SECRET_KEY=<SECRET_KEY>
# prod version requires AWS S3 configuration
# dev version saves files localy
DJANGO_SETTINGS_MODULE=simplify-tasks.settings.prod / simplify-tasks.settings.dev

# AWS
AWS_ACCESS_KEY_ID=<ID>
AWS_SECRET_ACCESS_KEY=<ACCESS_KEY>
AWS_STORAGE_BUCKET_NAME=<BUCKET_NAME>
RENDER_EXTERNAL_HOSTNAME=<HOST>
```

#### Configure project
```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

#### Configure prod project
```bash
# Save static files
python manage.py collectstatic
```


## Pages
Below are some key pages:

| Method | Endpoint            | Description            |
|--------|---------------------|------------------------|
| POST   | `/`  | Home page            |
| POST   | `/accounts/login/` | Login page |
| GET    | `/accounts/logot/`       | Logout page        |
| GET   | `/workers/`       | Worker list     |


## Running Tests
```bash
# Run all tests
python manage.py test tests
```

## Deployment
1. Configure `.env` file.
2. Use `gunicorn`/`wairess` and `nginx` for production deployment.
3. Configure database settings for PostgreSQL or another production database.
4. Use a cloud provider like AWS, DigitalOcean, or Heroku for hosting.

## Future Improvements
- Real time notification system
- Task type pages, CRUD
- Add files support for tasks
- Deep Role system
- Deep Test system

## License
This project is licensed under the MIT [License](LICENSE).



