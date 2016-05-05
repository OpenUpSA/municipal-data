"""
Django settings for municipal_finance project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'true') == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = '-r&cjf5&l80y&(q_fiidd$-u7&o$=gv)s84=2^a2$o^&9aco0o'
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

GOOGLE_ANALYTICS_ID = 'UA-48399585-37'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'municipal_finance',
    'scorecard',
    'wazimap_mapit',
    'wazimap.apps.WazimapConfig',
    'census',

    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'django_extensions',
    'corsheaders',
)

# Sites
# 2: Scorecard
# 3: API

if DEBUG:
    SITE_ID = int(os.environ.get('SITE_ID', '2'))

# Wazimap
from wazimap.settings import WAZIMAP
WAZIMAP['name'] = 'Municipal Money'
WAZIMAP['url'] = 'http://municipalmoney.org.za'
WAZIMAP['comparative_levels'] = []
WAZIMAP['country_code'] = 'ZA'
WAZIMAP['geometry_data'] = {}
# TODO: district
WAZIMAP['levels'] = {
    'country': {
        'children': ['province'],
    },
    'province': {
        'children': ['municipality', 'district'],
    },
    'district': {
        'children': ['municipality'],
    },
    'municipality': {
        'plural': 'municipalities',
    },
}
WAZIMAP['profile_builder'] = 'scorecard.profiles.get_profile'
WAZIMAP['ga_tracking_id'] = GOOGLE_ANALYTICS_ID
WAZIMAP['twitter'] = ''
WAZIMAP['geodata'] = 'scorecard.geo.GeoData'

MIDDLEWARE_CLASSES = (
    'municipal_finance.middleware.SiteMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'municipal_finance.middleware.ApiErrorHandler',
)

ROOT_URLCONF = 'municipal_finance.urls'

WSGI_APPLICATION = 'municipal_finance.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://municipal_finance:municipal_finance@localhost:5432/municipal_finance')
db_config = dj_database_url.parse(DATABASE_URL)
db_config['ATOMIC_REQUESTS'] = True
DATABASES = {
    'default': db_config,
}

# Caches
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-za'
TIME_ZONE = 'Africa/Johannesburg'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
FORMAT_MODULE_PATH = 'municipal_money.formats'


# CORS
CORS_ORIGIN_ALLOW_ALL = True


# Templates
TEMPLATE_DEBUG = DEBUG
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "wazimap.context_processors.wazimap_settings",
    "municipal_finance.context_processors.google_analytics",
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

ASSETS_DEBUG = DEBUG
ASSETS_URL_EXPIRE = False

# assets must be placed in the 'static' dir of your Django app

# where the compiled assets go
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# the URL for assets
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
)

PYSCSS_LOAD_PATHS = [
    os.path.join(BASE_DIR, 'municipal_finance', 'static'),
    os.path.join(BASE_DIR, 'municipal_finance', 'static', 'bower_components'),
    os.path.join(BASE_DIR, 'scorecard', 'static'),
    os.path.join(BASE_DIR, 'scorecard', 'static', 'bower_components'),
]

PIPELINE = {
    'STYLESHEETS': {
        'babbage': {
            'source_filenames': (
                'bower_components/fontawesome/css/font-awesome.css',
                'bower_components/babbage.ui/dist/deps.css',
                'bower_components/babbage.ui/dist/babbage.ui.css',
                'bower_components/babbage.ui/dist/embed.css',
                'stylesheets/explore.scss',
            ),
            'output_filename': 'babbage.css',
        },
        'docs': {
            'source_filenames': (
                'bower_components/fontawesome/css/font-awesome.css',
                'slate/stylesheets/screen.css',
                'stylesheets/docs.scss',
            ),
            'output_filename': 'docs.css',
        },
        'table': {
            'source_filenames': (
                'bower_components/fontawesome/css/font-awesome.css',
                'bower_components/bootstrap-sass/assets/stylesheets/_bootstrap.scss',
                'stylesheets/vendor/select2.min.css',
                'stylesheets/table.scss',
            ),
            'output_filename': 'table.css',
        },
    },
    'JAVASCRIPT': {
        'js': {
            'source_filenames': (
                'javascript/vendor/jquery-1.12.3.min.js',
                'javascript/app.js',
            ),
            'output_filename': 'app.js',
        },
        'babbage': {
            'source_filenames': (
                'javascript/vendor/jquery-1.12.3.min.js',
                'bower_components/babbage.ui/dist/deps.js',
                'bower_components/babbage.ui/dist/templates.js',
                'bower_components/babbage.ui/src/util.js',
                'bower_components/babbage.ui/src/app.js',
                'bower_components/babbage.ui/src/api.js',
                'bower_components/babbage.ui/src/babbage.js',
                'bower_components/babbage.ui/src/crosstab.js',
                'bower_components/babbage.ui/src/facts.js',
                'bower_components/babbage.ui/src/treemap.js',
                'bower_components/babbage.ui/src/sankey.js',
                'bower_components/babbage.ui/src/chart.js',
                'bower_components/babbage.ui/src/panel.js',
                'bower_components/babbage.ui/src/pager.js',
                'bower_components/babbage.ui/src/workspace.js',
            ),
            'output_filename': 'babbage.js',
        },
        'docs': {
            'source_filenames': (
                'javascript/vendor/jquery-1.12.3.min.js',
                'slate/javascripts/lib/_energize.js',
                'slate/javascripts/lib/_lunr.js',
                'slate/javascripts/lib/_jquery_ui.js',
                'slate/javascripts/lib/_jquery.tocify.js',
                'slate/javascripts/lib/_jquery.highlight.js',
                'slate/javascripts/lib/_imagesloaded.min.js',
                'slate/javascripts/app/_lang.js',
                'slate/javascripts/app/_search.js',
                'slate/javascripts/app/_toc.js',
                'javascript/docs.js',
            ),
            'output_filename': 'docs.js',
        },
        'table': {
            'source_filenames': (
                'javascript/vendor/jquery-1.12.3.min.js',
                'bower_components/underscore/underscore-min.js',
                'bower_components/backbone/backbone-min.js',
                'javascript/vendor/d3-format.min.js',
                'javascript/vendor/select2.min.js',
                'bower_components/bootstrap-sass/assets/javascripts/bootstrap.min.js',
                'javascript/table.js',
            ),
            'output_filename': 'table.js',
        },
    },
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,

    'COMPILERS': (
        'municipal_finance.pipeline.PyScssCompiler',
    ),
}

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'municipal_finance.pipeline.GzipManifestPipelineStorage'


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR'
    },
    'loggers': {
        'municipal_finance': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'wazimap': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'census': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'sqlalchemy.engine': {
            'level': 'INFO' if DEBUG else 'WARN',
        },
        'django': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        }
    }
}
