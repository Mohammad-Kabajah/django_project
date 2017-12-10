import threading
import uuid

__author__ = 'omar'

local = threading.local()

def get_current_request_id():
    return  local.request_id


def generate_request_id(request):
    return uuid.uuid4().hex

def force_set_current_request_id():
    local.request_id = uuid.uuid4().hex
