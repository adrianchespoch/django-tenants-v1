from pathlib import Path


# EnvV
import os
from dotenv import load_dotenv

load_dotenv()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# ## Load Envs from  .env  :
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
# ## Load Envs from  .env  :
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true')


ALLOWED_HOSTS = []


# Application definition =========================
SHARED_APPS = [
    # tenants
    'django_tenants',

    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # swagger
    'drf_yasg',

    # "django.contrib.admin",
    # "django.contrib.auth",
    # "django.contrib.contenttypes",
    # "django.contrib.sessions",
    # "django.contrib.messages",
    # "django.contrib.staticfiles",
    # "rest_framework",
    # 'rest_framework.authtoken',
    
    # multi-tenants: no need to be in TENANT_APPS
    'multicpy',
    
    "users",
    
]

TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # swagger
    'drf_yasg',
    
    # auth
    "users",
]

INSTALLED_APPS = list(set(SHARED_APPS)) + list(set([app for app in TENANT_APPS if app not in SHARED_APPS]))

# INSTALLED_APPS = [

#     # ### Shared Apps ---------------
#     # tenants
#     'django_tenants',

#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",

#     # ### ================= custom ================= ###
#     # DRF
#     'rest_framework',

#     # authtoken: alta compatibilidad con users d django
#     'rest_framework.authtoken',

#     # swagger
#     'drf_yasg',



#     # ### Tenants apps ---------------
#     # own django apps
#     'users',
    
#     # tenants
#     'multicpy',

# ]

MIDDLEWARE = [
    # ### multitenants ---------------
    'django_tenants.middleware.main.TenantMainMiddleware',
    'multicpy.middlewares.middleware.CustomTenantMiddleware',
    

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    # #### CORS headers: before CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",


    # ### Custom Middlewares
    # unauthorized middleware to unify 401 responses
    'backend.shared.middlewares.unauthorized_middleware.CustomUnauthorizedMiddleware',
    # 404 middleware
    'backend.shared.middlewares.not_found_middleware.Custom404Middleware',
    # forbidden middleware to unify 403 responses
    'backend.shared.middlewares.forbidden_middleware.CustomForbiddenMiddleware',

]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# ## Load Envs from  .env  :
DATABASES = {
    # ## PostgreSQL dockerized
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    },
}

# ## DB: tenants -----------
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# # Internationalization
# # https://docs.djangoproject.com/en/5.0/topics/i18n/

# LANGUAGE_CODE = "en-us"

# TIME_ZONE = "UTC"

# USE_I18N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"







# ### ### ### CUSTOM SETUP =================================================
# ### Internationalization
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True


# ### CORS Origin ---------------
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS').split(',')
# CORS_ALLOWED_ORIGINS = [
#     "http://192.168.31.212:5175",
#     "http://localhost:5175",
# ]
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
# ALLOWED_HOSTS = [
#     "127.0.0.1",
#     "localhost",
#     "192.168.31.212",
# ]
CORS_ALLOW_CREDENTIALS = True


# ### Swagger ---------------
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'SECURITY_REQUIREMENTS': [
        {
            'Token': []
        }
    ],
}


# ### Cache ---------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL'), 
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}



# ### Custom User Model: app.Model ---------------
# from .user_model import User <- in users/models/__init__.py
AUTH_USER_MODEL = 'users.User'



# ### REST Framework ---------------
REST_FRAMEWORK = {
    # 'cause we use DRF Token Auth and this avoids the need for CSRF.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}



# ### Multitenants ---------------
# ## Multitenants DB
TENANT_MODEL = 'multicpy.Scheme' # model q aplica el TenantMixin
TENANT_DOMAIN_MODEL = 'multicpy.Domain' # domain con pass



# ## Consts Multitenants 
DOMAIN = os.environ.get('DOMAIN') or 'localhost'
DEFAULT_SCHEMA = os.environ.get('DEFAULT_SCHEMA') or 'public'
