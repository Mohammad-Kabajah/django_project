from __future__ import division
from gettext import gettext
from math import ceil

from django.http import JsonResponse
from rest_framework.response import Response


class Messages:
    RESPONSE = {}
    RESPONSE[100] = {'message': gettext('CONTINUE')}
    RESPONSE[101] = {'message': gettext('SWITCHING_PROTOCOLS')}
    # RESPONSE[200] = {'message': gettext('OK')}
    RESPONSE[200] = {'message': gettext('SUCCESS')}
    RESPONSE[201] = {'message': gettext('CREATED')}
    RESPONSE[202] = {'message': gettext('ACCEPTED')}
    RESPONSE[203] = {'message': gettext('NON_AUTHORITATIVE_INFORMATION')}
    RESPONSE[204] = {'message': gettext('NO_CONTENT')}
    RESPONSE[205] = {'message': gettext('RESET_CONTENT')}
    RESPONSE[206] = {'message': gettext('PARTIAL_CONTENT')}
    RESPONSE[300] = {'message': gettext('MULTIPLE_CHOICES')}
    RESPONSE[301] = {'message': gettext('MOVED_PERMANENTLY')}
    RESPONSE[302] = {'message': gettext('FOUND')}
    RESPONSE[303] = {'message': gettext('SEE_OTHER')}
    # RESPONSE[304] = {'message': gettext('NOT_MODIFIED')}
    RESPONSE[304] = {'message': gettext('BAD_REQUEST')}
    RESPONSE[305] = {'message': gettext('USE_PROXY')}
    RESPONSE[306] = {'message': gettext('RESERVED')}
    RESPONSE[307] = {'message': gettext('TEMPORARY_REDIRECT')}
    RESPONSE[400] = {'message': gettext('BAD_REQUEST')}
    RESPONSE[401] = {'message': gettext('UNAUTHORIZED')}
    RESPONSE[402] = {'message': gettext('PAYMENT_REQUIRED')}
    RESPONSE[403] = {'message': gettext('FORBIDDEN')}
    RESPONSE[404] = {'message': gettext('NOT_FOUND')}
    RESPONSE[405] = {'message': gettext('METHOD_NOT_ALLOWED')}
    RESPONSE[406] = {'message': gettext('NOT_ACCEPTABLE')}
    RESPONSE[407] = {'message': gettext('PROXY_AUTHENTICATION_REQUIRED')}
    RESPONSE[408] = {'message': gettext('REQUEST_TIMEOUT')}
    RESPONSE[409] = {'message': gettext('CONFLICT')}
    RESPONSE[410] = {'message': gettext('GONE')}
    RESPONSE[411] = {'message': gettext('LENGTH_REQUIRED')}
    RESPONSE[412] = {'message': gettext('PRECONDITION_FAILED')}
    RESPONSE[413] = {'message': gettext('REQUEST_ENTITY_TOO_LARGE')}
    RESPONSE[414] = {'message': gettext('REQUEST_URI_TOO_LONG')}
    RESPONSE[415] = {'message': gettext('UNSUPPORTED_MEDIA_TYPE')}
    RESPONSE[416] = {'message': gettext('REQUESTED_RANGE_NOT_SATISFIABLE')}
    RESPONSE[417] = {'message': gettext('EXPECTATION_FAILED')}
    RESPONSE[428] = {'message': gettext('PRECONDITION_REQUIRED')}
    RESPONSE[429] = {'message': gettext('TOO_MANY_REQUESTS')}
    RESPONSE[431] = {'message': gettext('REQUEST_HEADER_FIELDS_TOO_LARGE')}
    RESPONSE[451] = {'message': gettext('UNAVAILABLE_FOR_LEGAL_REASONS')}
    RESPONSE[500] = {'message': gettext('INTERNAL_SERVER_ERROR')}
    RESPONSE[501] = {'message': gettext('NOT_IMPLEMENTED')}
    RESPONSE[502] = {'message': gettext('BAD_GATEWAY')}
    RESPONSE[503] = {'message': gettext('SERVICE_UNAVAILABLE')}
    RESPONSE[504] = {'message': gettext('GATEWAY_TIMEOUT')}
    RESPONSE[505] = {'message': gettext('HTTP_VERSION_NOT_SUPPORTED')}
    RESPONSE[511] = {'message': gettext('NETWORK_AUTHENTICATION_REQUIRED')}
    RESPONSE[600] = {'message': gettext('ERROR')}
    RESPONSE[1312] = {'message': gettext('INVALID_JSON')}


def harri_response(data, status_code, message_code=None, template_name=None, headers=None, exception=False, content_type=None):
    status_message = message_code if message_code else Messages.RESPONSE[status_code]['message']

    h_res = {'data':data, 'status': status_message, 'status_code': status_code}
    return Response(h_res, 200, template_name, headers, exception, content_type)


def harri_paginated_response(data, status_code, message_code=None, template_name=None,
                             headers=None, exception=False, content_type=None,
                             offset=None, limit=None, total_count=None):
    status_message = message_code if message_code else Messages.RESPONSE[status_code]['message']
    # Note the division import at top
    last_page = int(ceil(total_count / limit)) - 1 if total_count != 0 else 0
    current_page = int(ceil(offset / limit))

    data['per_page'] = limit
    data['total'] = total_count
    data['last_page'] = last_page
    data['current_page'] = current_page
    h_res = {'data': data, 'status': status_message, 'status_code': status_code}
    return Response(h_res, 200, template_name, headers, exception, content_type)


def harri_django_response(data, status_code, message_code=None):
    status_message = message_code if message_code else Messages.RESPONSE[status_code]['message']
    h_res = {'data': data, 'status': status_message, 'status_code': status_code}
    return JsonResponse(data=h_res, status=status_code)