from common.libs.harri_db import db_session
from app_name.models.models import Schedule, Station, Reservation
from sqlalchemy.orm import load_only, contains_eager, aliased, joinedload
from datetime import datetime
from sqlalchemy.orm import Load


class ReservationRepository(object):
    @staticmethod
    def get_reservation_by_id(schedule_id, load_only_tuple=None):
        if load_only_tuple == None:
            query = db_session.query(Schedule)
        else:
            query = db_session.query(Schedule).options(load_only(*(load_only_tuple)))
        reservation_request = query.filter(Schedule.id == schedule_id).one()
        return reservation_request

    @staticmethod
    def get_all_reservations():
        request = db_session.query(Schedule).all()
        return request

    @staticmethod
    def get_all_reservations_per_user(customer_id):
        station1 = aliased(Station)
        station2 = aliased(Station)
        query = db_session.query(Reservation)\
            .join(Schedule, Reservation.schedule_id == Schedule.id) \
            .join(station1, station1.id == Schedule.departure_station_id) \
            .join(station2, station2.id == Schedule.arrival_station_id) \
            .options(
            Load(Reservation).load_only("id").
                contains_eager(Schedule).load_only("id", "arrival_time", "departure_time", "price"),
            contains_eager(Schedule.departure_station, alias=station1).load_only("id", "name"),
            contains_eager(Schedule.arrival_station, alias=station2).load_only("id", "name")
                ).filter(Reservation.customer_id >= customer_id)

        request = query.all()
        return request

    @staticmethod
    def create_reservation(customer_id, schedule_id):
        try: # need to validate input
            reservation = Reservation()
            reservation.customer_id = customer_id
            reservation.schedule_id = schedule_id
            db_session.add(reservation)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            return False
        return True
