from . import local, generate_request_id
from boto3 import session
import app_name.constants

class RequestIDMiddleware(object):

    def process_request(self, request):
        self._process_boto_session()
        request_id = generate_request_id(request)
        local.request_id = request_id
        request.id = request_id

    def _process_boto_session(self):
        app_name.constants.BOTO_SESSION = session.Session()

    # def process_response(self, request, response):
    #     release_local(local)
    #     return response
    #     pass