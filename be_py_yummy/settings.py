"""
Django settings for be_py_yummy project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--)3n5-fago$u3zz*%+&1+#xejs)48k*k@=$$-xogogt09*tbg_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

VNPAY_TMN_CODE = 'D062FM6Y'  # Thay bằng vnp_TmnCode từ Sandbox
VNPAY_HASH_SECRET_KEY = 'ZGLPKDIR4V1PH6YXL9NVAFVKSQBQN6PP'  # Thay bằng vnp_HashSecret
VNPAY_PAYMENT_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
VNPAY_RETURN_URL = 'https://3d58-2001-ee1-db01-fd0-854d-a1a9-43df-30e3.ngrok-free.app/api/vnpay/return/' # Thay bằng URL ngrok
VNPAY_IPN_URL = 'https://3d58-2001-ee1-db01-fd0-854d-a1a9-43df-30e3.ngrok-free.app/api/vnpay/ipn/'  # Thay bằng URL ngrok

ALLOWED_HOSTS = [
    'ef38-2001-ee1-db03-4a90-d096-dc38-95f7-5042.ngrok-free.app',
    '127.0.0.1',  # localhost
    'localhost',  # local DNS
    '10.0.2.2',  # Địa chỉ IP của máy chủ trong môi trường giả lập Android (10.0.2.2 dùng cho Android Emulator)
    '3d58-2001-ee1-db01-fd0-854d-a1a9-43df-30e3.ngrok-free.app',  # Thêm URL ngrok
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'be_py_yummy.urls'
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-language',
    'content-type',
    'x-csrftoken',  # Nếu bạn sử dụng CSRF token
    'authorization',
    'access-control-allow-origin',
]

CORS_EXPOSE_HEADERS = [
    'access-control-allow-origin',  # Expose the header so frontend can access it
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'be_py_yummy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Chọn PostgreSQL
        'NAME': 'yummy',  # Tên cơ sở dữ liệu
        'USER': 'postgres',  # Tên người dùng PostgreSQL
        'PASSWORD': '210424',  # Mật khẩu người dùng
        'HOST': 'localhost',  # Địa chỉ của PostgreSQL (thường là localhost nếu chạy trên máy tính cá nhân)
        'PORT': '5432',  # Cổng mặc định của PostgreSQL
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
