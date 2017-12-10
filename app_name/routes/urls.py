from django.conf.urls import url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers

from app_name.views.v1.test_session_controller import BusView, StationView, StationScheduleView, ReserveScheduleView, \
    ReservationView


router = routers.SimpleRouter(trailing_slash=False)
# router.register(r'test_session', TestSessionView, base_name='test_session')
# urlpatterns = router.urls
# /bus, /station, /schedule, /reserve
router.register(r'bus', BusView, base_name='bus')
router.register(r'station', StationView, base_name='station')
router.register(r'schedule', ReserveScheduleView, base_name='schedule')
router.register(r'reservation', ReservationView, base_name='reservation')


# /station/pk/info
station_route = routers.NestedSimpleRouter(router, r'station', lookup='station', trailing_slash=False)
station_route.register(r'schedule', StationScheduleView, base_name='station schedule')


urlpatterns = []

urlpatterns += router.urls
urlpatterns += station_route.urls
