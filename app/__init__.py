import logging
import sentry_sdk
import traceback
from http import HTTPStatus
from flask import Flask, request, g
from config import configuration
from flask_jsonschema import JsonSchema, ValidationError
from app.helpers.models import ReturnData, ErrorCode
from logging.handlers import TimedRotatingFileHandler
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

app = Flask(__name__)
app.config.from_object(configuration)

app.config.from_object(__name__)
app.config.update(configuration.__dict__)
jsonschema = JsonSchema(app)

# logging
logger = logging.getLogger("app-logger")
logger.setLevel(logging.INFO)

@app.route('/')
def index():
    return "Hello!"


if configuration.DEBUG == False:
    handler = TimedRotatingFileHandler(configuration.LOG_DIR_PATH, 'midnight', 1, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.INFO)
    sentry_sdk.init(dsn=configuration.SENTRY_DSN, integrations=[sentry_logging], traces_sample_rate=1.0)

@app.before_request
def before_request():
    g.access_token = request.headers.get('Authorization', None)
    g.api_key = request.headers.get('Api-Key', None)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    header['Access-Control-Allow-Methods'] = '*'
    return response

@app.errorhandler(ValidationError)
def on_validation_error(e):
    resp = ReturnData()
    message = e.schema.get("messages", e.message)
    message = message if isinstance(message, str) else message.get(e.validator, e.message)
    if configuration.IS_PRODUCTION:
        err = traceback.format_exc()
        logger.error(str(err))
    else:
        print(str(message))
    resp.error_message = message
    resp.error_code = ErrorCode.validate_error
    return resp.serialize(HTTPStatus.INTERNAL_SERVER_ERROR, error_code=ErrorCode.error)


from app.modules.auth import module as auth_module

app.register_blueprint(auth_module)
