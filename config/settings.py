from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


def _split_env_list(value: str | None, default: list[str]) -> list[str]:
    if not value:
        return default
    return [item.strip() for item in value.split(',') if item.strip()]


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-musshop-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in {'1', 'true', 'yes'}
ALLOWED_HOSTS = _split_env_list(
    os.getenv('DJANGO_ALLOWED_HOSTS'),
    ["musshop.asia", "www.musshop.asia", "127.0.0.1", "localhost", "<89.207.251.140>"],
)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # наши приложения
    "catalog",
    "accounts",
    'cart', 
    'orders', 
    'apikeys',
    

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # подключим шаблон из ZIP сюда
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",

            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CART_SESSION_ID = "cart"

CSRF_TRUSTED_ORIGINS = _split_env_list(
    os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS'),
    ['https://musshop.asia', 'https://www.musshop.asia'],
)
CSRF_TRUSTED_ORIGINS = [
    "https://musshop.asia",
    "https://www.musshop.asia",
]