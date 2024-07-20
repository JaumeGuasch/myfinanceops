from django.urls import path, re_path
from finances import views
from finances.views import CreateOperationView, OperationsView, HomeView

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test-token', views.test_token),
    re_path('logout', views.logout),
    path('home', HomeView.as_view(), name='home'),
    path('create_operation', CreateOperationView.as_view(), name='create_operation'),
    path('operations', OperationsView.as_view(), name='operations_list'),
]
