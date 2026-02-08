from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WorkScheduleTypeViewSet,
    MyScheduleViewSet,
    HolidayViewSet,
    CalendarViewSet
)

router = DefaultRouter()
router.register(r'schedule/types', WorkScheduleTypeViewSet, basename='schedule-types')
router.register(r'schedule/holidays', HolidayViewSet, basename='holidays')

urlpatterns = [
    path('', include(router.urls)),
    path('schedule/my/', MyScheduleViewSet.as_view({'get': 'list', 'put': 'update'}), name='my-schedule'),
    path('schedule/calendar/', CalendarViewSet.as_view({'get': 'list'}), name='calendar'),
]

