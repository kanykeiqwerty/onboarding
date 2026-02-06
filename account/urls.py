from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('register/', views.RegistrationView.as_view()),
    path('superadmin/users/', views.SuperAdminUserView.as_view()),
    path('superadmin/users/<int:pk>/', views.SuperAdminUserView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('logout/', views.LogoutApiView.as_view()),
    # Управление админами (только суперадмин)
    path('admin/create/', views.AdminCreateView.as_view(), name='admin-create'),
    path('admin/list/', views.AdminListView.as_view(), name='admin-list'),
    path('admin/<int:pk>/', views.AdminDetailView.as_view(), name='admin-detail'),
    
    # Управление стажерами (админы и суперадмин)
    path('intern/create/', views.InternCreateView.as_view(), name='intern-create'),
    path('intern/list/', views.InternListView.as_view(), name='intern-list'),
    path('intern/<int:pk>/', views.InternDetailView.as_view(), name='intern-detail'),
    
    # Информация о текущем пользователе
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
]
