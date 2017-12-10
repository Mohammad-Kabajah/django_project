from common.libs.harri_db import db_session
from app_name.models.models import Schedule, Station
from sqlalchemy.orm import load_only, contains_eager, aliased, joinedload
from datetime import datetime
from sqlalchemy.orm import Load


class ScheduleRepository(object):
    @staticmethod
    def get_schedule_by_id(schedule_id, load_only_tuple=None):
        if load_only_tuple == None:
            query = db_session.query(Schedule)
        else:
            query = db_session.query(Schedule).options(load_only(*(load_only_tuple)))
        bus_request = query.filter(Schedule.id == schedule_id).one()
        return bus_request

    @staticmethod
    def get_all_schedule():
        request = db_session.query(Schedule).all()
        return request

    @staticmethod
    def get_all_available_schedule():

        from_date = datetime.now()

        station1 = aliased(Station)
        station2 = aliased(Station)

        query = db_session.query(Schedule)\
            .join(station1, station1.id == Schedule.departure_station_id) \
            .join(station2, station2.id == Schedule.arrival_station_id) \
            .options(
                Load(Schedule).load_only("id", "arrival_time", "departure_time", "price").
                contains_eager(Schedule.departure_station, alias=station1).load_only("id", "name"),
                contains_eager(Schedule.arrival_station, alias=station2).load_only("id", "name")
                ).filter(Schedule.departure_time >= from_date)

        # Equivalent SQL but no contains eager
        # query = db_session.query(Schedule)\
        #     .join(station1, station1.id == Schedule.departure_station_id) \
        #     .join(station2, station2.id == Schedule.arrival_station_id). \
        #     options(
        #     Load(Schedule).load_only("id", "arrival_time", "departure_time", "price"),
        #     Load(station1).load_only("id", "name"),
        #     Load(station2).load_only("id", "name"))\
        #     .filter(Schedule.departure_time >= from_date)

        request = query.all()
        return request

    @staticmethod
    def create_schedule(bus_id, departure_station_id, arrival_station_id, price, arrival_time, departure_time):
        try:
            schedule = Schedule()
            schedule.bus_id = bus_id
            schedule.departure_station_id = departure_station_id
            schedule.arrival_station_id = arrival_station_id
            schedule.price = price
            schedule.arrival_time = arrival_time
            schedule.departure_time = departure_time
            db_session.add(schedule)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            return False
        return True
