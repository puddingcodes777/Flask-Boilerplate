import random
import string
import re
import os
import base64
from datetime import datetime
from flask import request
from sqlalchemy import and_, or_
from pytz import timezone
from app.helpers.models import RecordStatus, UserPermission
from config import configuration
from datetime import timedelta
from unicodedata import normalize
from werkzeug.utils import secure_filename


class FormHelper:
    def __init__(self, form):
        self.message = ""
        for k, v in form.errors.items():
            self.message = str(v[0])

    def get_error_code(self):
        return self.message


def turkish_charset(data):
    data = data.replace("İ", "I") \
        .replace("Ş", "S") \
        .replace("Ğ", "G") \
        .replace("Ç", "C") \
        .replace("Ö", "O") \
        .replace("Ü", "U") \
        .replace("ı", "i") \
        .replace("ş", "s") \
        .replace("ğ", "g") \
        .replace("ç", "c") \
        .replace("ö", "o") \
        .replace("ü", "u")
    return data


class DateTime(datetime):
    @classmethod
    def now(*args, **kwargs):
        return datetime.now(timezone(configuration.TIMEZONE))


def generate_string_code(ranges=32, type=None):
    value = int(ranges)

    if type is None:
        case = string.ascii_lowercase
    elif "uppercase":
        case = string.ascii_uppercase

    return ''.join(random.choice(case + string.digits) for _ in range(value))


def get_user_control_allowed_action(token, permission):
    # from app import db
    # from app.db_models import UserAccessToken, User, UserRolePermission

    # user = User.query \
    #     .join(UserAccessToken, UserAccessToken.user_id == User.id) \
    #     .filter(or_(User.status == RecordStatus.active)) \
    #     .filter(and_(UserAccessToken.status == RecordStatus.active,
    #                  UserAccessToken.token == token,
    #                  UserAccessToken.expire_date > datetime.now(),
    #                  UserAccessToken.is_delete == False,
    #                  User.is_delete == False)) \
    #     .first()

    # if not user:
    #     return None
    # else:
    #     token_data = UserAccessToken.query.filter(UserAccessToken.token == token).first()
    #     token_data.expire_date = datetime.now() + timedelta(hours=configuration.ACCESS_TOKEN_EXPIRE_TIME)
    #     db.session.add(token_data)
    #     db.session.commit()

    #     if permission != UserPermission.none:
    #         permission_data = UserRolePermission.query \
    #             .filter(and_(UserRolePermission.user_role_id == user.user_role_id,
    #                          UserRolePermission.permission_type == permission[0],
    #                          UserRolePermission.status == RecordStatus.active,
    #                          UserRolePermission.is_delete == False,
    #                          UserRolePermission.permission_value == True)) \
    #             .first()

    #         if permission_data:
    #             return user
    #         else:
    #             return None
    #     else:
    #         return user
    return None


def generate_password(words=string.ascii_lowercase, length=8, numbers=string.digits, characters=None, first_upper=True):
    r = random.SystemRandom()
    elements = r.sample(words, length)

    if numbers:
        elements.insert(r.randint(1, len(elements)), r.choice(numbers))
    if characters:
        elements.insert(r.randint(1, len(elements)), r.choice(characters))
    if first_upper:
        elements[0] = elements[0].title()

    return ''.join(elements)


def generate_number_code(length=6):
    return ''.join(random.choice(string.digits) for _ in range(length))


def get_day_name(value):
    try:
        if int(value) == 1:
            return "Monday"
        elif int(value) == 2:
            return "Tuesday"
        elif int(value) == 3:
            return "Wednesday"
        elif int(value) == 4:
            return "Thursday"
        elif int(value) == 5:
            return "Friday"
        elif int(value) == 6:
            return "Saturday"
        elif int(value) == 7:
            return "Sunday"
        else:
            return ""
    except:
        return ""


def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'svg']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png', 'doc', 'docx', 'pdf', 'txt']


def slugify(text, id=None, delim='-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    result = []
    for word in _punct_re.split(turkish_charset(text.lower())):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word.decode(encoding='UTF-8'))

    result = delim.join(result)
    if id:
        result = result + delim + str(id)
    return result


def file_create_and_control(url, file, path):
    if file and (allowed_image(file.filename) or allowed_file(file.filename)):
        if url and os.path.exists(configuration.UPLOAD_FOLDER + url):
            os.remove(configuration.UPLOAD_FOLDER + url)
        image_url = secure_filename(file.filename)
        if not os.path.exists(configuration.UPLOAD_FOLDER + path):
            os.makedirs(configuration.UPLOAD_FOLDER + path)
        if not os.path.exists(configuration.UPLOAD_FOLDER + path + "/" + image_url):
            file.save(configuration.UPLOAD_FOLDER + path + "/" + image_url)
        return "/" + image_url if path == "/" else path + "/" + image_url
    else:
        return url


def base64_file_create(file, path):
    if not os.path.exists(configuration.UPLOAD_FOLDER + path):
        os.makedirs(configuration.UPLOAD_FOLDER + path)

    file_type = file.split(';')[0].split(':')[1]
    file_extension = file_type.split('/')[1]

    if file_extension.lower() == 'jpeg':
        image_url = '/' + generate_string_code() + '.jpg'
    elif file_extension.lower() == 'jpg':
        image_url = '/' + generate_string_code() + '.jpg'
    elif file_extension.lower() == 'png':
        image_url = '/' + generate_string_code() + '.png'
    elif file_extension.lower() == 'pdf':
        image_url = '/' + generate_string_code() + '.pdf'
    elif file_extension.lower() == 'xls':
        image_url = '/' + generate_string_code() + '.xls'
    elif file_extension.lower() == 'vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        image_url = '/' + generate_string_code() + '.xlsx'
    elif file_extension.lower() == 'doc':
        image_url = '/' + generate_string_code() + '.doc'
    elif file_extension.lower() == 'vnd.openxmlformats-officedocument.wordprocessingml.document':
        image_url = '/' + generate_string_code() + '.docx'
    else:
        image_url = 'example_file.' + file_extension

    starter = file.find(',')
    image_data = file[starter + 1:]
    base64_img_bytes = image_data.encode('utf-8')
    with open(configuration.UPLOAD_FOLDER + path + image_url, 'wb') as file_to_save:
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        file_to_save.write(decoded_image_data)

    return "/" + image_url if path == "/" else path + image_url


def get_file_size(file_path):
    size_in_bytes = os.path.getsize(configuration.UPLOAD_FOLDER + file_path)

    kb = round(size_in_bytes / 1024, 0)
    mb = round(size_in_bytes / (1024 * 1024), 1)
    gb = round(size_in_bytes / (1024 * 1024 * 1024), 1)
    bt = size_in_bytes

    if gb >= 1:
        return str(gb) + "gb"
    elif mb >= 1:
        return str(mb) + "mb"
    elif kb >= 1:
        return str(kb) + "kb"
    else:
        return str(bt) + "bt"
