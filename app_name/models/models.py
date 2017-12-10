from common.libs.harri_base_model import HBaseModel
from sqlalchemy import Column, String, Integer, Date, Enum, ForeignKey, Boolean, DateTime, DECIMAL, Numeric
from sqlalchemy.orm import relationship


class Bus(HBaseModel):
    __tablename__ = 'bus'

    category = Column(Enum('MINI', 'COACH'), default=None)
    plate_number = Column(String(7), nullable=True)

    schedules = relationship("Schedule", backref="bus")


class Customer (HBaseModel):
    __tablename__ = 'customer'

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(128), nullable=False)

    reservations = relationship("Reservation", backref="customer")


class Station (HBaseModel):
    __tablename__ = 'station'

    name = Column(String(32), nullable=False)
    city = Column(String(32), nullable=False)
    street = Column(String(32), nullable=False)
    latitude = Column(Numeric(precision=9, scale=6), nullable=False)
    longitude = Column(Numeric(precision=9, scale=6), nullable=False)


class Schedule (HBaseModel):
    __tablename__ = 'schedule'

    bus_id = Column(Integer, ForeignKey('bus.id'), nullable=False)
    departure_station_id = Column(Integer, ForeignKey('station.id'), nullable=False)
    arrival_station_id = Column(Integer, ForeignKey('station.id'), nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)

    reservations = relationship("Reservation", backref="schedule")
    departure_station = relationship("Station", foreign_keys=[departure_station_id], backref="departure_station_schedule")
    arrival_station = relationship("Station", foreign_keys=[arrival_station_id], backref="arrival_stations_schedule")


class Reservation (HBaseModel):
    __tablename__ = "reservation"

    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedule.id'), nullable=False)
