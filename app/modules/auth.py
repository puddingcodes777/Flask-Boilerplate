from http import HTTPStatus
from flask import Blueprint, request, g
from app import jsonschema
from app.helpers.models import ReturnData, RecordStatus, ErrorCode, UserPermission
from app.helpers.decorators import control_allowed_action

module = Blueprint('auth', __name__, url_prefix='/auth')

@module.route('/user-login', methods=['POST'])
@jsonschema.validate('auth', 'user_login')
def user_login():
    req = request.json
    res = ReturnData()
    return {}

@module.route('/user-logout', methods=['POST'])
@control_allowed_action(permission=UserPermission.none)
def user_logout():
    res = ReturnData()

    # Token...

    res.data = True
    return res.serialize()
