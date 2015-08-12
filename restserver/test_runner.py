from django.conf import settings
from discover_runner import DiscoverRunner

class FastTestRunner(DiscoverRunner):
    def setup_test_environment(self):
        super(FastTestRunner, self).setup_test_environment()
        # Don't write files
        settings.DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
        # Use a faster password hasher. This REALLY helps.
        settings.PASSWORD_HASHERS = (
            'django.contrib.auth.hashers.MD5PasswordHasher',
        )
