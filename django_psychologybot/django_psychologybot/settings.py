from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = 'ux)plafr!taa=pops7c#2ig19)j-3g(bd93q-6@%&v5bxb6x-+'

ALLOWED_HOSTS = ['s983114.srvape.com', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chatbot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_psychologybot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_psychologybot.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT = "staticfiles"
#STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/') 
# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    # Основное
    "site_title": "Bereke Admin",  
    "site_header": "Bereke Панель управления",
    "site_brand": "BerekeAdmin", 
    "site_logo": "/logo.ico", 
    "site_logo_classes": "img-circle", 
    "site_logo_width": "64px",  
    "site_logo_height": "64px",
    "welcome_sign": "Добро пожаловать в административный раздел Береке",


    "copyright": "© 2024 Bereke", 


    "topmenu_links": [
        {"name": "На сайт", "url": "/", "icon": "fas fa-globe"},  # Переход на сайт
    ],

    "show_sidebar": True,  
    "navigation_expanded": True,  
    "custom_links": {  
        "my_app": [
            {"name": "Статистика", "url": "/admin/my_app/report/", "icon": "fas fa-chart-bar"},
        ]
    },
    "custom_css": "admin/custom.css",
}