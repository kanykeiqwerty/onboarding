from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, EmployeeViewSet, WelcomeBlockViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'employees', EmployeeViewSet, basename='employees')
router.register(r'welcome', WelcomeBlockViewSet, basename='welcome')

urlpatterns = [
    path('', include(router.urls)),
]

