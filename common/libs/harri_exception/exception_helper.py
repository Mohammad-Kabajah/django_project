import traceback
import logging
from common.libs.harri_responses import harri_response
from django.http import Http404
from rest_framework.compat import set_rollback
from rest_framework import status
from common.libs.harri_logger.slack import SlackService
from rest_framework.exceptions import APIException
from django.utils import six
from django.core.exceptions import PermissionDenied


CRITICAL = 50
ERROR = 40
NOTSET = 0


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    headers = None
    if isinstance(exc, APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        message_code = exc.detail
        status_code = exc.status_code
        set_rollback()

    elif isinstance(exc, Http404):
        msg = _('Not found.')
        message_code = six.text_type(msg)
        status_code = status.HTTP_404_NOT_FOUND
        set_rollback()

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        message_code = six.text_type(msg)
        status_code = status.HTTP_403_FORBIDDEN
        set_rollback()

    else:
        message_code = str(exc)
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return harri_response({}, message_code=message_code, status_code=status_code, headers=headers)


# Any new custom exceptions should extend this on app level
class HarriAPIException(APIException):
    severity = CRITICAL


def harri_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, HarriAPIException) and exc.severity == CRITICAL or response.data['status_code'] == 500:
        SlackService.general_error_notify(context['request'], exc)

    # This for Harri convention, we always return the response with 200 status in its header, and the client will
    # always check the status code in the returned json
    response.status_code = 200

    # Log all errors
    logger = logging.getLogger(__name__)
    logger.error(str(exc.message) + "\n" + str(
        traceback.format_exc()) + "\n" + "------------------ happy debugging :) ------------------\n")

    return response
