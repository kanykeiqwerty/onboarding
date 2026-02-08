from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstructionViewSet

router = DefaultRouter()
router.register(r'instructions', InstructionViewSet, basename='instructions')

urlpatterns = [
    path('', include(router.urls)),
]

