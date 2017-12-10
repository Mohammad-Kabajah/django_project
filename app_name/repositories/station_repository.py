from common.libs.harri_db import db_session
from app_name.models.models import Station, Schedule
from sqlalchemy.orm import load_only, contains_eager, aliased
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import Load


class StationRepository(object):
    @staticmethod
    def get_station_by_id(station_id, load_only_tuple=None):
        if load_only_tuple == None:
            query = db_session.query(Station)
        else:
            query = db_session.query(Station).options(load_only(*(load_only_tuple)))
        bus_request = query.filter(Station.id == station_id).one()
        return bus_request

    @staticmethod
    def get_all_stations(load_only_tuple=None):
        if load_only_tuple == None:
            request = db_session.query(Station).all()
        else:
            request = db_session.query(Station).options(load_only(*(load_only_tuple))).all()
        return request

    @staticmethod
    def get_station_schedule(station_id):

        from_date = datetime.now()
        query = db_session.query(Station)\
            .join(Schedule, and_(Station.id == Schedule.departure_station_id,
                                 Station.id == station_id,
                                 Schedule.departure_time >= from_date))\
            .options(Load(Station).load_only("id", "name").
                     contains_eager(Station.departure_station_schedule).
                     load_only("arrival_time", "departure_time", "price").joinedload(Schedule.arrival_station).load_only("name"))

        request = query.all()
        return request
