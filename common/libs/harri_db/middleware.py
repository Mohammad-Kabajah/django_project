from common.libs.harri_db import db_session

__author__ = 'omar'


class DBSessionMiddleware(object):

    def process_response(self, request, response):
        db_session.remove()
        return response
