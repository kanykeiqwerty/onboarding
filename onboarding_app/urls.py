from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OnboardingDayViewSet, DailyReportViewSet

router = DefaultRouter()
router.register(r'onboarding/days', OnboardingDayViewSet, basename='onboarding-days')
router.register(r'reports', DailyReportViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
]

