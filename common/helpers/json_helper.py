import json

__author__ = 'omar'

def str_to_json(value):
    try:
        return json.loads(value)
    except Exception as err:
        print err
        return None


def json_to_str(value):
    try:
        if type(value) == str or type(value) == unicode:
            return value

        return json.dumps(value)
    except Exception as err:
        print "json_to_str:error", err
        return None