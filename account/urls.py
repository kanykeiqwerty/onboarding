from django.urls import path
from account.views import Views, AdminViews, InternViews
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('register/', views.RegistrationView.as_view()),
    path('superadmin/users/', Views.SuperAdminUserView.as_view()),
    path('superadmin/users/<int:pk>/', Views.SuperAdminUserView.as_view()),
    path('login/', Views.LoginApiView.as_view()),
    path('logout/', Views.LogoutApiView.as_view()),
    # Управление админами (только суперадмин)
    path('admin/create/', AdminViews.AdminCreateView.as_view(), name='admin-create'),
    path('admin/list/', AdminViews.AdminListView.as_view(), name='admin-list'),
    path('admin/<int:pk>/', AdminViews.AdminDetailView.as_view(), name='admin-detail'),
    
    # Управление стажерами (админы и суперадмин)
    path('intern/create/', InternViews.InternCreateView.as_view(), name='intern-create'),
    path('intern/list/', InternViews.InternListView.as_view(), name='intern-list'),
    path('intern/<int:pk>/', InternViews.InternDetailView.as_view(), name='intern-detail'),
    
    # Информация о текущем пользователе
    path('me/', Views.CurrentUserView.as_view(), name='current-user'),
    path('my_profile/', InternViews.MyProfileView.as_view(), name='my-profile' )
]
