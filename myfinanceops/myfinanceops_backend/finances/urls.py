from django.contrib import admin
from django.urls import path, include
from finances.views import LoginView, UserView, LogoutView, SignupView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
]
