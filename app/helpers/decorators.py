from flask import g
from functools import wraps
from app.helpers.models import ErrorCode
from app.helpers.models import ReturnData
from http import HTTPStatus
from app.helpers.extensions import get_user_control_allowed_action
from app.helpers.models import UserPermission
from app import configuration
from sqlalchemy import and_, or_
from app.helpers.models import RecordStatus, UserPermission


def control_allowed_action(permission=UserPermission.none):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            res = ReturnData()
            if g.access_token or g.api_key:
                if g.access_token:
                    user = get_user_control_allowed_action(token=g.access_token, permission=permission)
                    if user:
                        g.user = user
                        return f(*args, **kwargs)
                    else:
                        return res.serialize(HTTPStatus.UNAUTHORIZED, error_code=ErrorCode.forbidden)
                else:
                    if g.api_key == configuration.SECRET_KEY:
                        # from app.db_models import User
                        # user = User.query.filter(and_(User.id == 1, User.status == RecordStatus.active, User.is_delete == False)).first()
                        # g.user = user
                        return f(*args, **kwargs)
                    else:
                        return res.serialize(HTTPStatus.UNAUTHORIZED, error_code=ErrorCode.forbidden)

            return res.serialize(HTTPStatus.UNAUTHORIZED, error_code=ErrorCode.forbidden)

        return decorated_function

    return decorator
