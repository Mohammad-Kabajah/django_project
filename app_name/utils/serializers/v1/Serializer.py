from marshmallow import fields, pre_dump
from app_name.models.models import Bus, Customer, Station, Schedule, Reservation
from app_name.utils.serializers import AppSerializer


class ReservationSerializer(AppSerializer):

    class Meta:
        model = Reservation


class CustomerSerializer(AppSerializer):
    reservations = fields.Nested(ReservationSerializer, many=True)

    class Meta:
        model = Customer


class ScheduleSerializer(AppSerializer):
    reservations = fields.Nested(ReservationSerializer, many=True)
    @pre_dump
    def reformat(self, data):
        # print ("data.arrival_station", data.arrival_station)
        if self.only:
            if "arrival_station_data" in self.only:
                data.arrival_station_data = {"name": data.arrival_station.name}

            if "departure_station_data" in self.only:
                data.departure_station_data = {"name": data.departure_station.name}

    arrival_station_data = fields.Dict()
    departure_station_data = fields.Dict()

    class Meta:
        model = Schedule

ReservationSerializer.schedule = fields.Nested(ScheduleSerializer, many=False)
ReservationSerializer.customer = fields.Nested(CustomerSerializer, many=False)


class StationSerializer(AppSerializer):
    departure_station_schedule = fields.Nested(ScheduleSerializer, many=True)
    arrival_stations_schedule = fields.Nested(ScheduleSerializer, many=True)

    class Meta:
        model = Station

ScheduleSerializer.departure_station = fields.Nested(StationSerializer, many=False)
ScheduleSerializer.arrival_station = fields.Nested(StationSerializer, many=False)


class BusSerializer(AppSerializer):
    schedules = fields.Nested(ScheduleSerializer, many=True)

    class Meta:
        model = Bus
