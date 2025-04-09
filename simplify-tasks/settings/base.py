import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-z29iyf4vhl0q16ssm9v&l2@exaqq2wkirx$m(qtxz(zt%wzf2f")

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "manager",
]

JAZZMIN_SETTINGS = {
    "site_title": "s-tasks-admin",
    "site_header": "Simplify Tasks",
    "site_brand": "Simplify Tasks",
    "welcome_sign": "Welcome to Simplify Tasks admin panel",
    "site_logo": "images/main-logo.png",
    "login_logo": "images/main-logo.png",
    "login_logo_dark": None,
    "topmenu_links": [
        {"name": "Main Page", "url": "/"},
    ],
    "show_sidebar": True,
    "changeform_format": "vertical_tabs",
    "show_ui_builder": True,
    "related_modal_active": True,
    "user_avatar": "profile_picture",
    "icons": {
        "manager.Worker": "fa-solid fa-user",
        "manager.Position": "fa-solid fa-briefcase",
        "manager.Task": "fa-solid fa-list-check",
        "manager.Project": "fa-solid fa-folder",
        "manager.Tag": "fa-solid fa-tag",
        "manager.Team": "fa-solid fa-users",
        "manager.TaskType": "fa-solid fa-list",
    }
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-navy",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "darkly",
    "dark_mode_theme": "solar",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "manager.middlewares.UpdateLastActivityMiddleware"
]

ROOT_URLCONF = "simplify-tasks.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "simplify-tasks.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "manager.Worker"

SESSION_COOKIE_AGE = 3600 * 24 * 7
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

LOGIN_REDIRECT_URL = "/profile/"
