"""
this package contains all the api views
"""
from django.conf import settings
from django.http import JsonResponse
from common.exceptions import ForbiddenException
from common.libs.harri_responses import harri_response, harri_django_response
from common.libs.validator.extreme_validator import ExtremeValidator
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import SessionAuthentication
from common.helpers import mobile_helper

class CSRFAuthentication(SessionAuthentication):
    """
        Overriding SessionAuthentication to make use of their feature of forcing CSRF  
    """

    def authenticate(self, request):
        is_mobile_app = mobile_helper.is_mobile_app(request)
        if is_mobile_app:
            return ({}, "")

        try:
            csrf_token = request.COOKIES[settings.CSRF_COOKIE_NAME]
        except KeyError:
            csrf_token = None

        if csrf_token is not None and "team_user_id" in request.session:
            self.enforce_csrf(request)

        return ({}, "")


class AppNameViewSet(ViewSet):
    """
    This is base class for all views
    """

    # define authentication classes, if you want to disable CSRf just remove the following line
    authentication_classes = () #(CSRFAuthentication,)

    def __init__(self, api_access_scope='user', requires_authentication=True, validation_schema=None, method_names=None):
        if validation_schema is None:
            validation_schema = {}
        self.method_names = method_names
        if method_names is None:
            self.method_names = ()

        super(AppNameViewSet, self).__init__(api_access_scope=api_access_scope,
                                         requires_authentication=requires_authentication,
                                         validation_schema=validation_schema,
                                         method_names=self.method_names)

    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?
        try:
            self.initial(request, *args, **kwargs)
            action_name = self.action if self.action else request.method.lower()
            # Apply authentication and validation
            if action_name in self.method_names:
                # Authenticate
                if self.requires_authentication:
                    globals()["authenticate_" + self.api_access_scope](request)

                # Validate
                validation_method = self.validation_schema.get(action_name)
                if validation_method:
                    error_messages = validate_request(request, validation_method)
                    if error_messages:
                        return harri_django_response(error_messages, 400)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


def authenticate_user(request):
    session_store = request.session
    # TODO EDIT THIS AS REQUIRED
    if "team_user_id" not in session_store:
        raise ForbiddenException()

    return True


def authenticate_admin(request):
    session_store = request.session
    if "admin_id" not in session_store:
        raise ForbiddenException()

    return True


def validate_request(request, validation_schema):
    validator = ExtremeValidator()
    if request.method in ["GET", "DELETE"]:
        request_data = request.query_params
    else:
        request_data = request.data
    return validator.validate_extreme(request_data, validation_schema)
"""
this package contains all the api views
"""




def health_check(request):
    return JsonResponse({"status": "SUCCESS"})
