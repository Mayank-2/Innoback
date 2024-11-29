from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserLogout,UserProfileView


urlpatterns = [
    path('api/users/register', UserRegistrationView.as_view(), name='register'),
    path('api/users/login', UserLoginView.as_view(), name='login'),
    path('api/users/logout',UserLogout.as_view(),name="userLogout"),
    path('api/users/profile',UserProfileView.as_view(),name="userProfile"),
]