from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from app_name.constants import ApiAccessScope
from app_name.views import AppNameViewSet
from common.libs.harri_responses import harri_response
from app_name.components.BusComponent import BusComponent
from app_name.components.StationComponent import StationComponent
from app_name.components.ScheduleComponent import ScheduleComponent
from app_name.components.ReservationComponent import ReservationComponent
from app_name.utils.serializers.v1.Serializer import BusSerializer, StationSerializer, ScheduleSerializer, \
    ReservationSerializer
from datetime import datetime
__author__ = 'darwazeh'


class BusView(AppNameViewSet):
    def __init__(self, **kwargs):
        super(BusView, self).__init__(api_access_scope=ApiAccessScope.USER,
                                      requires_authentication=False,
                                      method_names=('list', 'retrieve', 'create', 'destroy', 'update'),
                                      validation_schema={})
        self.bus_component = BusComponent()
        self.bus_serializer = BusSerializer()

    # GET /bus
    def list(self, request):
        print (request)
        buses = self.bus_component.get_all_buses()
        data = self.bus_serializer.dump(buses, many=True).data
        return harri_response(data, 200)

    # GET /bus/pk
    def retrieve(self, request, pk):
        print (request)
        bus = self.bus_component.get_bus_by_id(pk)
        data = self.bus_serializer.dump(bus, many=False).data
        print (data)
        return harri_response(data, 200)


class StationView(AppNameViewSet):
    def __init__(self, **kwargs):
        super(StationView, self).__init__(api_access_scope=ApiAccessScope.USER,
                                          requires_authentication=False,
                                          method_names=('list', 'retrieve', 'create', 'destroy', 'update'),
                                          validation_schema={})
        self.station_component = StationComponent()

    # GET /stations
    def list(self, request):
        print (request)
        station_serializer = StationSerializer(only=("id", "name"))
        stations = self.station_component.get_all_stations_name()
        data = station_serializer.dump(stations,  many=True).data
        print (data)
        return harri_response(data, 200)

    # GET /station/pk
    def retrieve(self, request, pk):
        station_serializer = StationSerializer(only=("id", "name", "street", "city"))
        print (request)
        station = self.station_component.get_station_by_id(pk)
        data = station_serializer.dump(station, many=False).data
        print (data)
        return harri_response(data, 200)


class StationScheduleView(AppNameViewSet):
    def __init__(self, **kwargs):
        super(StationScheduleView, self).__init__(api_access_scope=ApiAccessScope.USER,
                                                  requires_authentication=False,
                                                  method_names=('list', 'retrieve', 'create', 'destroy', 'update'),
                                                  validation_schema={})
        self.station_component = StationComponent()

    # GET /station/pk/schedule
    def list(self, request, station_pk, **kwargs):
        station_serializer = StationSerializer(only=("id", "name", 'departure_station_schedule'))
        station_serializer.fields['departure_station_schedule'].only = ['arrival_time', 'departure_time', 'price',
                                                                        'arrival_station_data']

        station = self.station_component.get_station_schedule(station_id=station_pk)[0]
        data = station_serializer.dump(station,  many=False).data
        return harri_response(data, 200)


class ReserveScheduleView(AppNameViewSet):
    validation_schema = {
        'create':{
            'bus_id':
                ['int', 'required'],
            'departure_station_id':
                ['int', 'required'],
            'arrival_station_id':
                ['int', 'required'],
            'price':
                ['int', 'required'],
            "arrival_time":
                ['string', 'required', {'date_format':'%Y-%m-%dT%H:%M:%S.%fZ'}],#'%Y-%m-%dT%H:%M:%S.%fZ'
            "departure_time":
                ['string', 'required', {'date_format':'%Y-%m-%dT%H:%M:%S.%fZ'}]
                # ['string', 'required', 'iso_date']
        }
    }
    def __init__(self, **kwargs):
        super(ReserveScheduleView, self).__init__(api_access_scope=ApiAccessScope.USER,
                                                  requires_authentication=False,
                                                  method_names=('list', 'create'),
                                                  validation_schema=self.validation_schema)
        self.schedule_component = ScheduleComponent()

    # GET /schedule
    def list(self, request, **kwargs):
        schedule_serializer = ScheduleSerializer(only=("id", "arrival_time", "departure_time",
                                                       "price", 'departure_station_data', 'arrival_station_data'))
        schedule_serializer.fields['departure_station_data'].only = ['name']
        schedule_serializer.fields['arrival_station_data'].only = ['name']

        schedules = self.schedule_component.get_all_available_schedule()
        data = schedule_serializer.dump(schedules,  many=True).data
        return harri_response(data, 200)

    # POST /schedule
    def create(self, request):
        print (request.data)
        bus_id = request.data.get('bus_id')
        departure_station_id = request.data.get('departure_station_id')
        arrival_station_id = request.data.get('arrival_station_id')
        price = request.data.get('price')
        arrival_time = datetime.strptime(request.data.get('arrival_time'), '%Y-%m-%dT%H:%M:%S.%fZ')
        departure_time = datetime.strptime(request.data.get('departure_time'), '%Y-%m-%dT%H:%M:%S.%fZ')

        created = self.schedule_component.create_schedule(bus_id=bus_id,
                                                          departure_station_id=departure_station_id,
                                                          arrival_station_id=arrival_station_id,
                                                          price=price,
                                                          arrival_time=arrival_time,
                                                          departure_time=departure_time)

        if not created:
            return harri_response("Error creating new schedule", 500)
        return harri_response("created Successfully", 200)


class ReservationView(AppNameViewSet):
    validation_schema = {
        'create':{
            'customer_id':
                ['int', 'required'],
            'schedule_id':
                ['int', 'required']
        }
    }

    def __init__(self, **kwargs):
        super(ReservationView, self).__init__(api_access_scope=ApiAccessScope.USER,
                                              requires_authentication=False,
                                              method_names=('list', 'retrieve', 'create', 'destroy', 'update'),
                                              validation_schema=self.validation_schema)
        self.reservation_component = ReservationComponent()

    # GET /reservation
    # def list(self, request, **kwargs):
    #     reservations_serializer = ReservationSerializer(only=("id", "schedule", "customer"))
    #     # reservations_serializer.fields['departure_station_data'].only = ['name']
    #     # reservations_serializer.fields['arrival_station_data'].only = ['name']
    #
    #     reservations = self.reservation_component.get_all_reservations()
    #     data = reservations_serializer.dump(reservations,  many=True).data
    #     return harri_response(data, 200)

    # POST /reservation
    def create(self, request):
        print (request.data)
        customer_id = request.data.get('customer_id')
        schedule_id = request.data.get('schedule_id')

        created = self.reservation_component.create_reservation(customer_id=customer_id, schedule_id=schedule_id)

        if not created:
            return harri_response("Error creating new reservation", 500)
        return harri_response("created Successfully", 200)

    # GET /reservation/pk
    def retrieve(self, request, pk):
        # id 2xstation_names 2xtimes
        reservation_serializer = ReservationSerializer(only=("id", "name", "street", "city"))
        print (request)
        reservations = self.reservation_component.get_reservation_by_id(pk)
        data = reservation_serializer.dump(reservations, many=False).data
        return harri_response(data, 200)
