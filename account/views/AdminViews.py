from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.pagination import PageNumberPagination

from django.contrib.auth import get_user_model
from account import serializers
from account.permission import IsAdmin, IsSuperAdmin


class StandartResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


User = get_user_model()