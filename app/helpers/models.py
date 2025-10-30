import json
from app.helpers.encoders import JsonEncoder
from http import HTTPStatus
from enum import IntEnum, Enum
from flask import Response


class Empty:
    pass


class StudentStatus:
    passive = 0
    inactive = 1
    active = 2
    approve = 3


class StudentMessageSender:
    university_department = 1
    student = 2


class RecordStatus:
    passive = 0
    active = 1


class MediaType:
    folder = 1
    file = 2


class SlugType:
    content_category = 1
    content_content = 2


class Gender:
    none = 0
    male = 1
    female = 2


class LinkTarget:
    parent = '_parent'
    blank = '_blank'


class LinkType:
    content_category = 1
    content = 2
    other = 3
    external = 4


class LinkOther:
    contact = 1
    about = 2


class MenuGroup:
    main_left = 1
    main_right = 2
    footer = 3


class SliderGroup:
    main = 1


class SliderType:
    image = 1
    video = 2


class ImageType:
    image = 1
    video = 2


class ExternalVideoType:
    youtube = 1


class RedirectionCode:
    moved_permanently = 301


class UniversityLocation:
    none = 0
    southeast = 1
    midwest = 2
    newEngland = 3
    boston = 4
    midAtlantic = 5


class UserPermission:
    # NOTE: item[0] = permission_type, item[1]=group, item[2]=name,

    none = (0, 'None', 'None')

    # user permission
    user_role_list = (1000, 'User', 'Role List')
    user_role_get = (1001, 'User', 'Role Get')
    user_role_save = (1002, 'User', 'Role Save')
    user_role_delete = (1003, 'User', 'Role Delete')
    user_user_list = (1004, 'User', 'User List')
    user_user_get = (1005, 'User', 'User Get')
    user_user_save = (1006, 'User', 'User Save')
    user_user_delete = (1007, 'User', 'User Delete')
    user_role_permission = (1008, 'User', 'User Role Permission')

    # language permission
    language_list = (2000, 'Language', 'List')
    language_get = (2001, 'Language', 'Get')
    language_save = (2002, 'Language', 'Save')
    language_delete = (2003, 'Language', 'Delete')

    # settings permission
    settings_settings_get = (3000, 'Settings', 'Settings Get')
    settings_settings_save = (3001, 'Settings', 'Settings Save')
    settings_redirection_list = (3002, 'Settings', 'Redirection List')
    settings_redirection_get = (3003, 'Settings', 'Redirection Get')
    settings_redirection_save = (3004, 'Settings', 'Redirection Save')
    settings_redirection_delete = (3005, 'Settings', 'Redirection Delete')

    # menu permission
    menu_menu_list = (4000, 'Menu', 'Menu List')
    menu_menu_get = (4001, 'Menu', 'Menu Get')
    menu_menu_save = (4002, 'Menu', 'Menu Save')
    menu_menu_delete = (4003, 'Menu', 'Menu Delete')

    # slider permission
    slider_list = (5000, 'Slider', 'Slider List')
    slider_get = (5001, 'Slider', 'Slider Get')
    slider_save = (5002, 'Slider', 'Slider Save')
    slider_delete = (5003, 'Slider', 'Slider Delete')

    # address permission
    address_country_list = (6000, 'Address', 'Country List')
    address_country_get = (6001, 'Address', 'Country Get')
    address_country_save = (6002, 'Address', 'Country Save')
    address_country_delete = (6003, 'Address', 'Country Delete')
    address_states_list = (6004, 'Address', 'States List')
    address_states_get = (6005, 'Address', 'States Get')
    address_states_save = (6006, 'Address', 'States Save')
    address_states_delete = (6007, 'Address', 'States Delete')

    # content category permission
    content_category_list = (7000, 'Content', 'Category List')
    content_category_get = (7001, 'Content', 'Category Get')
    content_category_save = (7002, 'Content', 'Category Save')
    content_category_delete = (7003, 'Content', 'Category Delete')

    content_category_image_list = (7100, 'Content', 'Category Image List')
    content_category_image_get = (7101, 'Content', 'Category Image Get')
    content_category_image_save = (7102, 'Content', 'Category Image Save')
    content_category_image_delete = (7103, 'Content', 'Category Image Delete')

    # content permission
    content_content_list = (7500, 'Content', 'Content List')
    content_content_get = (7501, 'Content', 'Content Get')
    content_content_save = (7502, 'Content', 'Content Save')
    content_content_delete = (7503, 'Content', 'Content Delete')

    content_content_image_list = (7600, 'Content', 'Content Image List')
    content_content_image_get = (7601, 'Content', 'Content Image Get')
    content_content_image_save = (7602, 'Content', 'Content Image Save')
    content_content_image_delete = (7603, 'Content', 'Content Image Delete')

    # media permission
    media_label_list = (8000, 'Media', 'Media Label')
    media_label_save = (8001, 'Media', 'Media Label Save')
    media_label_delete = (8002, 'Media', 'Media Label Delete')

    media_list = (8003, 'Media', 'Media')
    media_save = (8004, 'Media', 'Media Save')
    media_delete = (8005, 'Media', 'Media Delete')

    # university permission
    university_list = (9000, 'University', 'List')
    university_get = (9001, 'University', 'Get')
    university_save = (9002, 'University', 'Save')
    university_delete = (9003, 'University', 'Delete')

    # sports permission
    sports_list = (9000, 'Sports', 'List')
    sports_get = (9001, 'Sports', 'Get')
    sports_save = (9002, 'Sports', 'Save')
    sports_delete = (9003, 'Sports', 'Delete')

    # student permission
    student_list = (9000, 'Student', 'List')
    student_get = (9001, 'Student', 'Get')
    student_save = (9002, 'Student', 'Save')
    student_delete = (9003, 'Student', 'Delete')


class ResponseStatus:
    error = 'error'
    success = 'success'


class ErrorCode(IntEnum):
    def __new__(cls, value, phrase, message=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.message = message
        return obj

    none = 0, 'no error', 'Operation complete successfully'
    no_records_found = 1, 'no record', 'No records found'
    bad_request = 2, 'bad request', 'No parameters.'
    error = 3, 'error', 'There is an error please try again'
    forbidden = 5, 'forbidden', 'Access forbidden'
    validate_error = 6, 'validate error', 'validate error'

    # user related messages
    login_fail = 1001, 'login fail', 'incorrect email or password.'
    user_not_found = 1002, 'not found', 'user not found'
    user_email_already_used = 1003, 'Email is already used', 'Email is already used'
    expire_link = 1006, 'Your link has been expired.', 'Your link has been expired.'
    expire_sms_code = 1007, 'Your sms code has been expired.', 'Your sms code has been expired.'
    invalid_current_password = 1008, 'Invalid current password', 'Invalid current password'

    # Json Validator messages
    json_field_required = 2000, 'field required', 'Please fill all required fields'
    json_password_format = 2001, 'password format', 'Password must have least 1 letter'


class ReturnData(object):
    def __init__(self, **kwargs):
        self.status = ResponseStatus.success
        self.error_code = ErrorCode.none
        self.error_message = None
        if kwargs.get('data', None):
            dt = json.loads(kwargs.get('data', None))
            self.data = dt.get('data', None)
        else:
            self.data = kwargs.get('data', None)
        self.total_count = 0
        self.status_code = HTTPStatus.OK
        self.fields = []

    def serialize(self, status_code=None, error_code=ErrorCode.none, child=False, fields=None):

        if fields is None:
            fields = []
        if not error_code:
            error_code = self.error_code

        if not status_code:
            status_code = self.status_code

        if not self.error_message:
            self.error_message = error_code.message

        if not fields:
            fields = self.fields

        if status_code == HTTPStatus.OK:
            self.status = ResponseStatus.success
            self.error_message = error_code.message
        else:
            self.status = ResponseStatus.error
            self.error_code = error_code if not error_code == ErrorCode.none else error_code.value
            if self.error_code == ErrorCode.error.value:
                self.error_message = ErrorCode.error.message

        del self.status_code
        del self.fields

        resp = Response(
            json.dumps(json.loads(JsonEncoder(child=child, field_params=fields).encode(self.__dict__)), sort_keys=True,
                       indent=4), status=status_code, mimetype='application/json')

        return resp


class HttpError(object):
    def __init__(self):
        self.Ok = 200
        self.BadRequest = 400
        self.Unauthorized = 401
        self.Forbidden = 403
        self.NotFound = 404
        self.NotAcceptable = 406
        self.ExpectationFailed = 417
        self.InternalServerError = 500
        self.NotImplemented = 501


class RedisDataTypes(Enum):
    all = -1
    flush_db = -2
    flush_all = -3
    address = -4
    cms = -5
    address_country = 1
    address_states = 2
    cms_menu = 3
    slug = 4
    cms_category = 5
    cms_content = 6
    cms_slider = 7
    settings = 8
