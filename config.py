import os

class DefaultConfig(object):
    def __init__(self):
        self.DEBUG = True
        self.BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        self.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
        self.JSONSCHEMA_DIR = os.path.join(self.BASE_DIR, 'app', 'schemas')
        self.LOG_DIR_PATH = "#"
        self.SENTRY_DSN = "#"

class ProductionConfig(DefaultConfig):
    def __init__(self):
        super(ProductionConfig, self).__init__()
        self.DEBUG = False

env = os.getenv('ENVIRONMENT', 'Development')
if env == "Development":
    configuration = DefaultConfig()
else:
    configuration = ProductionConfig()