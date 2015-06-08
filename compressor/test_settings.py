import os
import django

TEST_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'compressor',
    'coffin',
]
if django.VERSION < (1, 8):
    INSTALLED_APPS.append('jingo')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(TEST_DIR, 'static')

TEMPLATE_DIRS = (
    # Specifically choose a name that will not be considered
    # by app_directories loader, to make sure each test uses
    # a specific template without considering the others.
    os.path.join(TEST_DIR, 'test_templates'),
)

if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

SECRET_KEY = "iufoj=mibkpdz*%bob952x(%49rqgv8gg45k36kjcg76&-y5=!"

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)

MIDDLEWARE_CLASSES = []

if django.VERSION >= (1, 8):

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "DIRS": TEMPLATE_DIRS,
        },
        {
            "BACKEND": "django.template.backends.jinja2.Jinja2",
            "APP_DIRS": True,
            "DIRS": [
                os.path.join(TEST_DIR, 'test_templates_jinja2'),
            ],
            "OPTIONS": {
                "environment": "compressor.test_settings.jinja2_environment",
                "autoescape": False,
                "extensions": [
                    # Extensions needed for the test cases only.
                    "compressor.offline.jinja2.SpacelessExtension",
                    "compressor.contrib.jinja2ext.CompressorExtension",
                    "jinja2.ext.with_",
                    "jinja2.ext.do",
                ]
            }
        },
    ]

    def COMPRESS_JINJA2_GET_ENVIRONMENT():
        from django.template import engines

        return engines['jinja2'].env


def jinja2_environment(**options):
    import jinja2
    from compressor.offline.jinja2 import url_for

    env = jinja2.Environment(**options)
    env.globals['url_for'] = url_for

    return env
