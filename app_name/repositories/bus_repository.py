from sqlalchemy.orm import load_only

from common.libs.harri_db import db_session
from app_name.models.models import Bus


class BusRepository(object):
    @staticmethod
    def get_bus_by_id(bus_id, load_only_tuple):
        if load_only_tuple == None:
            query = db_session.query(Bus)
        else:
            query = db_session.query(Bus).options(load_only(*(load_only_tuple)))

        bus_request = query.filter(Bus.id == bus_id).one()
        return bus_request

    @staticmethod
    def get_all_buses():
        bus_request = db_session.query(Bus).all()
        return bus_request
