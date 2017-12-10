from app_name.repositories.bus_repository import BusRepository
from app_name.repositories.schedule_repository import ScheduleRepository
from app_name.repositories.station_repository import StationRepository


class ScheduleComponent(object):

    def __init__(self):
        pass

    def get_schedule_by_id(self, schedule_id):
        station = ScheduleRepository.get_schedule_by_id(schedule_id=schedule_id, load_only_tuple=("id", "name", "street", "city"))
        return station

    def get_all_schedule(self):
        schedules = ScheduleRepository.get_all_schedule()
        return schedules

    def get_all_available_schedule(self):
        schedules = ScheduleRepository.get_all_available_schedule()
        return schedules

    def create_schedule(self, bus_id, departure_station_id, arrival_station_id, price, arrival_time, departure_time):
        try:
            _ = BusRepository.get_bus_by_id(bus_id=bus_id, load_only_tuple=("id",)).id
        except Exception as e:
            raise Exception("Invalid bus id")

        try:
            _ = StationRepository.get_station_by_id(station_id=departure_station_id, load_only_tuple=("id",)).id
        except Exception as e:
            raise Exception("Invalid departure_station_id")

        try:
            StationRepository.get_station_by_id(station_id=arrival_station_id, load_only_tuple=("id",)).id
        except Exception as e:
            raise Exception("Invalid arrival_station_id")

        created = ScheduleRepository.create_schedule(bus_id=bus_id,
                                                     departure_station_id=departure_station_id,
                                                     arrival_station_id=arrival_station_id,
                                                     price=price,
                                                     arrival_time=arrival_time,
                                                     departure_time=departure_time)
        return created
