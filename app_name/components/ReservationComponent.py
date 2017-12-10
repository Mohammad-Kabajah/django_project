from app_name.repositories.reservation_repository import ReservationRepository
from app_name.repositories.schedule_repository import ScheduleRepository
from app_name.repositories.customer_repository import CustomerRepository
class ReservationComponent(object):

    def __init__(self):
        pass

    def get_reservation_by_id(self, schedule_id):
        station = ReservationRepository.get_reservation_by_id(schedule_id=schedule_id, load_only_tuple=("id", "name", "street", "city"))
        return station

    def get_all_reservations(self):
        schedules = ReservationRepository.get_all_reservations()
        return schedules

    def get_all_reservations_per_user(self, customer_id):
        schedules = ReservationRepository.get_all_reservations_per_user(customer_id)
        return schedules

    def create_reservation(self, customer_id, schedule_id):
        try:
            _ = CustomerRepository.get_customer_by_id(customer_id=customer_id, load_only_tuple=("id",)).id
        except Exception as e:
            raise Exception("Invalid bus id")

        try:
            _ = ScheduleRepository.get_schedule_by_id(schedule_id=schedule_id, load_only_tuple=("id",)).id
        except Exception as e:
            raise Exception("Invalid schedule_id")

        created = ReservationRepository.create_reservation(customer_id=customer_id,
                                                           schedule_id=schedule_id)
        return created
