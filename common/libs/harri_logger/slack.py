import traceback
from common.helpers.request_helper import build_header
from django.conf import settings
from django_slack import slack_message
from app_name.constants import SlackTemplates
from common.helpers.json_helper import json_to_str
import logging

__author__ = 'omar'


class SlackService:
    def __init__(self):
        pass

    @staticmethod
    def general_error_notify(request, exc):
        messages = SlackService.build_general_messages(request, exc)

        attachments = [
            {
                "fields": messages,
                "color": "danger",
                "mrkdwn_in": ["text", "pretext", "fields"]
            }
        ]

        SlackService.send_slack_message(SlackTemplates.GENERAL, messages, attachments)

    @staticmethod
    def simple_message(message):
        messages = [
            {
                'title': 'Error message',
                'value': "``` " + message + " ``` ",
            },
            {
                'title': 'Environment',
                'value': "``` " + settings.ENV + " ``` ",
            },
        ]
        attachments = [
            {
                "fields": messages,
                "color": "danger",
                "mrkdwn_in": ["text", "pretext", "fields"]
            }
        ]

        SlackService.send_slack_message(SlackTemplates.GENERAL, '', attachments)


    @staticmethod
    def send_slack_message(template, context=None, attachments=None):

        try:
            slack_message(template, context, attachments)
        except Exception as err:
            logging.getLogger('common').error(
                "Slack message failed, raised exception: {0}, with stack trace: {1}".format(err,
                                                                                            traceback.format_exc()))

    @staticmethod
    def build_general_messages(request, exc):
        headers = build_header(request)
        messages = [
            {
                'title': 'API',
                'value': "``` " + request.path + " ``` ",
            },
            {
                'title': 'Environment',
                'value': "``` " + settings.ENV + " ``` ",
            },
            {
                'title': 'User',
                'value': "``` " + 'N/A' + " ``` ",  # todo get user id from session
            },
            {
                'title': 'Error description',
                'value': "``` " + str(exc.message) + " ``` ",
            },
            {
                'title': 'Request headers',
                'value': "``` " + json_to_str(headers) + " ``` ",
            },
            {
                'title': 'User Agent',
                'value': "``` " + headers['HTTP_USER_AGENT'] + " ``` ",
            },
            {
                'title': 'Request body',
                'value': "``` " + json_to_str(dict(request.data)) + " ``` ",
            },
            {
                'title': 'Query Params',
                'value': "``` " + json_to_str(dict(request.query_params)) + " ``` ",
            },
            {
                'title': 'Stack trace',
                'value': "``` " + traceback.format_exc() + " ``` ",
            },

        ]

        return messages
