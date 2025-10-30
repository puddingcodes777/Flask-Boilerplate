import json
import datetime
import decimal
from werkzeug.datastructures import MultiDict
from enum import Enum


def request_encoder(obj):
    if isinstance(obj, dict):
        data = MultiDict()
        for k, v in obj.items():
            data.add(k, v)
        return data
    else:
        return obj


def check_field(x):
    return not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class'


def is_serializable(data):
    try:
        json.dumps(data)
        return True
    except TypeError:
        return False


class JsonEncoder(json.JSONEncoder):
    def __init__(self, child=False, field_params=[]):
        super(JsonEncoder, self).__init__()
        self.child = child
        self.field_params = field_params

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = obj.replace(microsecond=0).isoformat()
        elif isinstance(obj, decimal.Decimal):
            encoded_object = float(obj)
        elif isinstance(obj, Enum):
            encoded_object = obj.name
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object
