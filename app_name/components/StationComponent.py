from app_name.repositories.station_repository import StationRepository


class StationComponent(object):

    def __init__(self):
        pass

    def get_station_by_id(self, station_id):
        station = StationRepository.get_station_by_id(station_id=station_id, load_only_tuple=("id", "name", "street", "city"))
        return station

    def get_all_stations_name(self):
        stations = StationRepository.get_all_stations(load_only_tuple=('id', 'name'))
        return stations

    def get_station_schedule(self, station_id):
        station = StationRepository.get_station_schedule(station_id=station_id)
        return station

