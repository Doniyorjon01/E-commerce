
from datetime import timedelta
from pathlib import Path
from environs import Env
import os

BASE_DIR = Path(__file__).resolve().parent.parent
env = Env()
env.read_env()
SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DEBUG")
# DEBUG=True
DB_NAME = env.str("DB_NAME")
DB_USERNAME = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST", "db")
DB_PORT = env.str("DB_PORT")
REDIS_HOST = env.str("REDIS_HOST", "redis")
REDIS_PORT = env.str("REDIS_PORT")

# FCM_SERVER_KEY=env.str("FCM_SERVER_KEY")

CORS_ALLOW_ALL_ORIGINS = True # boshqa domendan kirishga ruxsat beradi. backend->backend.com, frontend->frontend.com. faqat true yoki false qabul qiladi
# CORS_ORIGIN_ALLOW_ALL = True # CORS_ALLOW_ALL_ORIGINS bu bilan bir xil ishlatish shart emas
CORS_ALLOW_CREDENTIALS = True  # Cookie, Session yoki Token bilan so‘rov yuborishga ruxsat berish.
# CORS_ALLOWED_ORIGINS = list(map(str, env.str("CORS_ALLOWED_ORIGINS").split(' '))) # malum domenlar uchun ishlaydi

ALLOWED_HOSTS =  list(map(str, env.str("ALLOWED_HOSTS").split(' ')))
  #Bu ro‘yxatda qaysi domen yoki IP orqali sizning backendga kirishga ruxsat borligini yozasiz.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
CORS_ALLOW_HEADERS = "*" # Har qanday header bilan so‘rov yuborishga ruxsat.



APPEND_SLASH = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    'accounts',

    # Out apps
    "rest_framework",
    "rest_framework_simplejwt",
    # "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "django_filters",
    'channels',
    'corsheaders',

]

#SECURE_SSL_REDIRECT = True
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60*24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(weeks=1),
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",

]
ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
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
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

ASGI_APPLICATION = "config.asgi.application"


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}



AUTH_USER_MODEL = "accounts.User"


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
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# MEDIA_URL = "media/"
# MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
PASSWORD_RESET_TIMEOUT = 259200
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)



AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False


from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os


# S3 config

# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")  # Timeweb S3 endpoint URL

# # Fayllarni S3'ga yuklash uchun storages sozlamasi
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# # Media URL
# MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"

# # S3 Qo'shimcha sozlamalar
# AWS_S3_ADDRESSING_STYLE = "virtual"
# AWS_QUERYSTRING_AUTH = True

# import os
# from datetime import datetime

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_DIR = os.path.join(BASE_DIR, "logs")
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "[{asctime}] {levelname} {name} | {message}",
#             "style": "{"
#         },
#         "access": {
#             "format": "[{asctime}] {levelname} {name} | {method} {path} {status_code}",
#             "style": "{"
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         },
#         "file_debug": {
#             "class": "logging.handlers.TimedRotatingFileHandler",
#             "filename": os.path.join(LOG_DIR, "debug.log"),
#             "when": "midnight",
#             "backupCount": 30,
#             "formatter": "verbose",
#             "encoding": "utf8",
#         },
#         "file_errors": {
#             "class": "logging.handlers.TimedRotatingFileHandler",
#             "filename": os.path.join(LOG_DIR, "errors.log"),
#             "when": "midnight",
#             "backupCount": 30,
#             "level": "ERROR",
#             "formatter": "verbose",
#             "encoding": "utf8",
#         },
#         "file_requests": {
#             "class": "logging.handlers.TimedRotatingFileHandler",
#             "filename": os.path.join(LOG_DIR, "requests.log"),
#             "when": "midnight",
#             "backupCount": 15,
#             "formatter": "access",
#             "encoding": "utf8",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console", "file_debug", "file_errors"],
#             "level": "DEBUG",
#             "propagate": True,
#         },
#         "django.request": {
#             "handlers": ["file_errors"],
#             "level": "ERROR",
#             "propagate": False,
#         },
#         "django.server": {
#             "handlers": ["file_debug"],
#             "level": "INFO",
#             "propagate": False,
#         },
#         "custom.request": {
#             "handlers": ["file_requests"],
#             "level": "INFO",
#             "propagate": False,
#         },
#     }
# }
