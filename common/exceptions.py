from common.libs.harri_exception.exception_helper import HarriAPIException, ERROR
__author__ = 'adarwazeh'


class ForbiddenException(Exception):
    pass

class UnAuhtorizedException(HarriAPIException):
    severity = ERROR
    status_code = 401
    default_detail = "You are not authorized"


class ResourceException(HarriAPIException):
    severity = ERROR
    status_code = 600
