from datetime import datetime
import json
from django.utils.encoding import smart_str


class ValidatorTool:
    model = None

    def __init__(self):
        pass

    def validate(self, _values, _fields_to_validate):
        response = []
        for field in _fields_to_validate:
            try:
                value = _values[field]

                output = getattr(self, "validate_field_" + field)(value)
                # output = u""+output
                if not output or type(output) is str or type(output) is unicode:
                    _fieldDict = dict()
                    _fieldDict["field"] = field
                    _fieldDict["error"] = output
                    response.append(_fieldDict)

            except KeyError:
                _fieldDict = dict()
                _fieldDict["field"] = field
                _fieldDict["error"] = 'missing {field}'.format(field=str(field))
                response.append(_fieldDict)

        return response

    def validateComplex(self, _values, _fields_to_validate):

        response = []
        for field in _fields_to_validate:
            try:
                output = getattr(self, "validate_field_" + field)(_values)

                if not output or type(output) is str or type(output) is unicode:
                    _fieldDict = dict()
                    _fieldDict["field"] = field
                    _fieldDict["error"] = output
                    response.append(_fieldDict)

            except KeyError:
                _fieldDict = dict()
                _fieldDict["field"] = field
                _fieldDict["error"] = 'missing {field}'.format(field=field)
                response.append(_fieldDict)
        return response

    def validate_unique_field(self, model, field_name, value):

        res = model.query.filter(getattr(model, field_name) == value).first()

        if res is None:
            return True

        return False

    def check_length_between(self, minimum, maximum, value):
        str_length = len(value)
        if str_length < minimum or str_length > maximum:
            return False

        return True

    def check_length_more_then(self, minimum, value):
        if len(value) < minimum:
            return False
        return True

    def is_empty(self, value):

        try:

            value = unicode(value, 'utf8')

            if len(value.strip()) == 0:
                return False
        except:
            return True

        return True

    def is_boolean(self, value):
        if value in [0, 1, "0", "1", "true", "false"]:
            return True

        return False

    def is_numeric(self, value):

        try:
            float(value)  # for int, long and float
        except ValueError:
            return False

        try:
            complex(value)  # for complex
        except ValueError:
            return False

        return True

    def check_length_less_than(self, maximum, value):
        if len(value) > maximum:
            return False
        return True

    def check_is_array(self, arr):
        return isinstance(arr, list)

    def check_is_array_of_int(self, arr):
        return all(isinstance(item, int) for item in arr)

    def check_is_array_of_str(self, arr):
        return all(isinstance(item, str) for item in arr)

    def check_is_array_of_unicode(self, arr):
        return all(isinstance(item, unicode) for item in arr)

    def check_is_array_of_dicts(self, arr):
        return all(isinstance(item, dict) for item in arr)

    def check_is_array_of_numeric(self, arr):
        return all(self.is_numeric(item) for item in arr)

    def validate_field_offset(self, _values):
        if 'offset' not in _values:
            return True

        if _values['offset'] is None:
            return ("offset can't be null")

        if not self.is_numeric(_values['offset']):
            return ("offset is invalid")

        return True

    def validate_field_limit(self, _values):

        if 'limit' not in _values:
            return True

        if _values['limit'] is None:
            return ("limit can't be null")

        if not self.is_numeric(_values['limit']):
            return ("limit must be numeric")

        if _values['limit'] < 0:
            return ("limit can't be less than 0")

        return True

    def validate_field_page(self, _values):
        if 'page' not in _values:
            return True

        if _values['page'] is None:
            return ("page can't be null")

        if not self.is_numeric(_values['page']):
            return ("page is invalid")

        if _values['page'] < 0:
            return ("page is invalid")

        return True

    # validate key exist and not empty
    def validate_key_exist_and_not_none(self, field, request):
        if field not in request or request[field] is None:
            return False

        return True


class ExtremeValidator(ValidatorTool):
    model = None

    def __init__(self):
        pass

    def check_is_array_of_str(self, arr):
        return all(self.is_string(item) for item in arr)

    def check_is_array_of_dicts(self, arr):
        return all(isinstance(item, dict) for item in arr)

    def validate_extreme(self, _values, validation_schema):
        # Sample validation schema
        # validation_schema = {
        #     "job_application_id": ["required", "numeric"],
        #     "name": ["string"],
        #     "start_date": ["date"]
        #     "place": ["dict"]
        #     "id": ["int"],
        #     "job_schedule_slot_id": ["required", "numeric", {"max_length": 200}],
        #     "brand_ids": ["required", "array_of_numeric"],
        #     "some_ids": ["required", "array_of_int"],
        #     "some_strings": ["required", "array_of_str"]
        # }

        response = []
        for key, value in validation_schema.iteritems():
            # validate if the fields is passed and if is null
            error_message = self.check_is_null(key, _values)
            if not error_message or type(error_message) is str or type(error_message) is unicode:
                self.add_error_to_response(key, error_message, response)
                continue

            if key == 'extra_validation':
                error_message = self.validate_extra(schema=value, request_data=_values)
                if not error_message or type(error_message) is str or type(error_message) is unicode:
                    self.add_error_to_response(key, error_message, response)
                    break
                continue

            for rule in value:

                if isinstance(rule, str):
                    if not hasattr(self, "validate_rule_" + rule):
                        raise Exception(rule + " rule is not implemented")
                    error_message = getattr(self, "validate_rule_" + rule)(key, _values)
                    if not error_message or type(error_message) is str or type(error_message) is unicode:
                        self.add_error_to_response(key, error_message, response)
                        break

                elif isinstance(rule, dict):
                    rule_key = rule.keys()[0]
                    rule_value = rule.values()[0]

                    if not hasattr(self, "validate_rule_" + rule_key):
                        raise Exception(rule_key + " rule is not implemented")

                    error_message = getattr(self, "validate_rule_" + rule_key)(key, rule_value, _values)
                    if type(error_message) is str or type(error_message) is unicode or (
                            type(error_message) is list and len(error_message) > 0) or not error_message:
                        self.add_error_to_response(key, error_message, response)
                        break

        return response

    def add_error_to_response(self, field, error, error_response):
        _fieldDict = dict()
        _fieldDict["field"] = field
        _fieldDict["error"] = error
        error_response.append(_fieldDict)

    def check_is_array_of_numeric(self, arr):
        return all(self.is_numeric(item) for item in arr)

    def is_string(self, value):
        try:
            smart_str(value)
        except ValueError:
            return False
        return True

    def check_is_null(self, value, _values):
        if value in _values and _values[value] is None:
            return value + " should not be null"
        return True

    def validate_rule_required(self, value, _values):
        if value not in _values:
            return value + " is required"
        return True

    def validate_rule_numeric(self, value, _values):
        if value in _values and not self.is_numeric(_values[value]):
            return value + " should be numeric"
        return True

    def validate_rule_int(self, value, _values):
        if value in _values and not isinstance(_values[value], int):
            return value + " should be int"
        return True

    def validate_rule_string(self, value, _values):
        if value in _values:
            if not self.is_string(_values[value]):
                return value + " should be string"
        return True

    def validate_rule_positive_num(self, value, _values):
        if value in _values:
            if _values[value] <= 0:
                return value + " should be positive"
        return True

    def validate_rule_zero_or_positive_num(self, value, _values):
        if value in _values:
            if _values[value] < 0:
                return value + " should be positive or zero"
        return True

    def validate_rule_not_empty(self, value, _values):
        if value in _values:
            try:
                if len(_values[value]) == 0:
                    return value + " should not be empty"
            except:
                if len(str(_values[value])) == 0:
                    return value + " should not be empty"
        return True

    def validate_rule_boolean(self, value, _values):
        if value in _values and not self.is_boolean(_values[value]):
            return value + " should be boolean"
        return True

    def validate_rule_array_of_numeric(self, value, _values):
        if value in _values:
            if len(_values[value]) == 0:
                return value + " should not be empty"
            if not self.check_is_array_of_numeric(_values[value]):
                return value + " should be array of numeric"
        return True

    def validate_rule_array_of_int(self, value, _values):
        if value in _values:
            if len(_values[value]) == 0:
                return value + " should not be empty"
            if not self.check_is_array_of_int(_values[value]):
                return value + " should be array of integers"
        return True

    def validate_rule_array_of_str(self, value, _values):
        if value in _values:
            if len(_values[value]) == 0:
                return value + " should not be empty"
            if not self.check_is_array_of_str(_values[value]):
                return value + " should be array of strings"
        return True

    def validate_rule_max_length(self, value, rule_value, _values):
        if value in _values:
            if len(_values[value]) > rule_value:
                return value + " could not be more than " + str(rule_value) + " characters"
        return True

    def validate_rule_possible_values(self, value, rule_values, _values):
        if value in _values:
            if _values[value] not in rule_values:
                return value + " should be one of " + ', '.join([str(x) for x in rule_values])
        return True

    def validate_rule_array_of_dicts(self, value, _values):
        if value in _values:
            if len(_values[value]) == 0:
                return value + " should not be empty"
            if not self.check_is_array_of_dicts(_values[value]):
                return value + " should be array of objects"
        return True

    def validate_rule_dict(self, value, _values):
        if value in _values and not isinstance(_values[value], dict):
            return value + " should be an object"
        return True

    def validate_rule_brand_or_google_place(self, value, _values):
        if "brand_name" not in _values and "google_place" not in _values:
            return "Neither brand_name nor google_place is sent"
        return True

    def validate_rule_institution_or_google_place(self, value, _values):
        if "institution_name" not in _values and "google_place" not in _values:
            return "Neither institution_name nor google_place is sent"
        return True

    def validate_rule_schema(self, key, rules, _values):
        if key in _values:
            for item in _values[key]:
                error_message = self.validate_extreme(item, rules)
                if error_message:
                    return error_message

        return True

    def validate_extra(self, schema, request_data):
        for rule, value in schema.iteritems():
            _rule = "validate_rule_extra_" + rule
            if not hasattr(self, _rule):
                raise Exception(rule + " rule is not implemented")

            error_message = getattr(self, _rule)(request_data=request_data,value=value)
            if not error_message or type(error_message) is str or type(error_message) is unicode:
                return error_message

        return True

    def validate_rule_extra_contain_at_least_one(self, request_data, value):
        request_field_set = set([key for key in request_data])
        required_fields_set = set(value)
        intersect = required_fields_set.intersection(request_field_set)

        if len(intersect) == 0:
            return "At least one of these fields must be given [" + ', '.join(value) + ']'

        return True

    def validate_rule_date_format(self, value, rule_value, _values):
        if value in _values:
            to_validate_list = _values[value]
            if not isinstance(to_validate_list, list):
                to_validate_list = [to_validate_list]

            for to_validate_value in to_validate_list:
                try:
                    datetime.strptime(to_validate_value, rule_value)
                except:
                    return "Incorrect date format, should be {format}".format(format=rule_value)

        return True

    def validate_rule_required_if(self, value, rule_values, _values):
        """
        The field under validation must be present if the field field is equal to any value.
        :param value:
        :param rule_values:
        :param _values:
        :return:
        """
        accumulative_bool = True
        for rule_item in rule_values:
            for rule_key, rule_value in rule_item.iteritems():
                accumulative_bool = accumulative_bool and rule_value == _values[rule_key]
        if accumulative_bool and value not in _values:
            return "Invalid data, '{validation_field}' should be present when {rules}".\
                        format(validation_field=value,
                               rules=" and ".join([json.dumps(rule_value) for rule_value in rule_values]))

        return True

    def validate_rule_different(self, value, rule_values, _values):
        """
        The given field must be different than the field under validation.
        :param value: field under validation
        :param rule_values: rule values
        :param _values: payload
        :return:
        """
        if value in _values:
            to_validate_list = rule_values
            for to_validate_value in to_validate_list:
                if _values[value] == _values[to_validate_value]:
                    return "Invalid data, {value} value should be different than {to_validate_value}".\
                        format(value=value, to_validate_value=to_validate_value)

        return True

    def validate_rule_after_date_time(self, value, rule_values, _values):
        """
        The field under validation must be a value after a specific date, or payload date
        :param value:
        :param rule_values:
        :param _values:
        :return:
        """
        if value in _values:
            start_date_obj = datetime.strptime(_values[value], "%b %d, %Y %H:%M")
            # If it's a string then find it in payload and compare with it
            if isinstance(rule_values[0], basestring):
                if rule_values[0] in _values:
                    end_date_string = _values[rule_values[0]]
                else:
                    return "Invalid data, can't compare date because {rule_value} is not found".\
                        format(rule_value=rule_values[0])
            else:
                end_date_string = rule_values[0]['date_time']
            if start_date_obj < datetime.strptime(end_date_string, "%b %d, %Y %H:%M"):
                return "Invalid data, {start_date} should be after {end_date}".\
                    format(start_date=value, end_date=end_date_string)
        return True

    def validate_rule_must_if_missing(self, value, rule_values, _values):
        """
        The field under validation must be present when any of the other specified fields are not present
        :param value:
        :param _values:
        :return:
        """
        value_exists = value in _values
        must_present = False
        to_validate_list = rule_values
        for to_validate_value in to_validate_list:
            if to_validate_value not in _values:
                must_present = True
                break
        if must_present and not value_exists:
            return "Invalid data, {value} must be present when {rules} are not provided". \
                format(value=value, rules=" and ".join([json.dumps(rule_value) for rule_value in rule_values]))
        return True

    def validate_rule_must_if_missing_all(self, value, rule_values, _values):
        """
        The field under validation must be present only if all of the other specified fields are not present
        :param value:
        :param _values:
        :return:
        """
        value_exists = value in _values
        must_present = True
        to_validate_list = rule_values
        for to_validate_value in to_validate_list:
            if to_validate_value in _values:
                must_present = False
                break
        if must_present and not value_exists:
            return "Invalid data, {value} must be present when {rules} are not provided". \
                format(value=value, rules=" and ".join([json.dumps(rule_value) for rule_value in rule_values]))
        return True

    def validate_rule_required_with(self, value, rule_values, _values):
        """
        The field under validation can be present only if any of the other specified fields are present
        :param value:
        :param _values:
        :return:
        """
        if value in _values:
            can_exist = False
            to_validate_list = rule_values
            for to_validate_value in to_validate_list:
                if to_validate_value in _values:
                    can_exist = True
                    break
            if not can_exist:
                return "Invalid data, {value} must be present with {rules}". \
                    format(value=value, rules=" and ".join([json.dumps(rule_value) for rule_value in rule_values]))
        return True

    def validate_rule_required_with_all(self, value, rule_values, _values):
        """
        The field under validation can be present only if all of the other specified fields are present
        :param value:
        :param _values:
        :return:
        """
        if value in _values:
            to_validate_list = rule_values
            for to_validate_value in to_validate_list:
                if to_validate_value not in _values:
                    return "Invalid data, {value} must be present with {rules}". \
                        format(value=value, rules=" and ".join([json.dumps(rule_value) for rule_value in rule_values]))
        return True

    def validate_rule_required_without(self, value, rule_values, _values):
        """
        If the field under validation present then any of other specified fields can not be present
        :param value:
        :param _values:
        :return:
        """
        if value in _values:
            can_exist = False
            to_validate_list = rule_values
            for to_validate_value in to_validate_list:
                if to_validate_value not in _values:
                    can_exist = True
                    break
            if not can_exist:
                return "Invalid data, {value} must not be present with {rules}". \
                    format(value=value, rules=" and ".join([json.dumps(rule_value) for rule_value in rule_values]))
        return True

    def validate_rule_required_without_all(self, value, rule_values, _values):
        """
        If the field under validation present then all of other specified fields can not be present
        :param value:
        :param _values:
        :return:
        """
        if value in _values:
            to_validate_list = rule_values
            for to_validate_value in to_validate_list:
                if to_validate_value in _values:
                    return "Invalid data, {value} must not be present with {rules}". \
                        format(value=value, rules=" and ".join([json.dumps(rule_value) for rule_value in rule_values]))
        return True

    def validate_rule_iso_date(self, value, _values):
        """

        :param value:
        :param _values:
        :return:
        """
        if value in _values and _values[value]:
            try:
                datetime.strptime(_values[value], '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                return "Incorrect date format, should be ISO date format"

        return True
