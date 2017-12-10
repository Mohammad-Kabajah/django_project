from app_name.repositories.bus_repository import BusRepository


class BusComponent(object):

    def get_bus_by_id(self, bus_id):
        bus = BusRepository.get_bus_by_id(bus_id=bus_id)
        return bus

    def get_all_buses(self):
        bus = BusRepository.get_all_buses()
        return bus
