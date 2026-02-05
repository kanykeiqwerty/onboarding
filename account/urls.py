from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
   
    path('login/', views.LoginApiView.as_view()),
    path('logout/', views.LogoutApiView.as_view()),
    # path('refresh/', TokenRefreshView.as_view()),
    # path('forgot/', views.ForgotPasswordView.as_view()),
    # path('restore/', views.RestorePasswordView.as_view()),

    # path('spam-follow/', views.FollowSpamApi.as_view()),
    

    # pathot/', views.ForgotPasswordView.as_view()),
    # path('restore('forg/', views.RestorePasswordView.as_view()),
]
