from django.contrib import admin
from django.urls import path, include
from finances.views import LoginView, LogoutView, SignupView, CreateOperationView, OperationsView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('create_operation/', CreateOperationView.as_view(), name='create_operation'),
    path('operations/', OperationsView.as_view(), name='operations_list'),

]
