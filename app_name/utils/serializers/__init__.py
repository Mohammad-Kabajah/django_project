from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

__author__ = 'omar'


class AppSerializer(ModelSchema):
    created = fields.DateTime(format="%b %d, %Y %H:%M:%S", attribute="created")
    updated = fields.DateTime(format="%b %d, %Y %H:%M:%S", attribute="updated")
