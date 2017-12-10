from common.libs.harri_db import db_session
from app_name.models.models import Customer
from sqlalchemy.orm import load_only, contains_eager, aliased, joinedload
from datetime import datetime
from sqlalchemy.orm import Load


class CustomerRepository(object):
    @staticmethod
    def get_customer_by_id(customer_id, load_only_tuple=None):
        if load_only_tuple == None:
            query = db_session.query(Customer)
        else:
            query = db_session.query(Customer).options(load_only(*(load_only_tuple)))
        customer_request = query.filter(Customer.id == customer_id).one()
        return customer_request

