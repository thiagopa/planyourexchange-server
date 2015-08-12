"""
    Copyright (C) 2015, Thiago Pagonha,
    Plan Your Exchange, easy exchange to fit your budget
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.
    
    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from test.test_utils import DisableMigrations
# Mocking default S3 storage for tests with inmemory storage because it's faster
DEFAULT_FILE_STORAGE = 'tests.test_utils.TestStorage'

# Faster password hasher for creating test users
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Faster inmemory database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
    }
}

# Loading only what is relevant to tests, so the app loads faster
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'rest_framework.authtoken',
    'restserver',
)

SECRET_KEY='TEST_KEY'

# Mirror rest framework basic configuration for tests
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

ROOT_URLCONF = 'restserver.urls'

# Disabling migrations for faster tests
MIGRATION_MODULES = DisableMigrations()