from django.urls import path, re_path
from finances import views
from finances.views import CreateOperationView, OperationsView, HomeView, OperationTypesView, get_operation_fields

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test-token', views.test_token),
    re_path('logout', views.logout),
    path('home', HomeView.as_view(), name='home'),
    path('create-operation', CreateOperationView.as_view(), name='create_operation'),
    path('operations', OperationsView.as_view(), name='operations_list'),
    path('operation-types', OperationTypesView.as_view(), name='operation-types'),
    path('operation-fields/', get_operation_fields, name='operation-fields'),
    path('get-all-operation-chain', views.get_all_operation_chain),
    path('get-markets', views.get_markets),
    path('create-market', views.create_market),
    path('delete-market', views.delete_market),
    path('get-commissions', views.get_commissions),
    path('create-commission', views.create_commission),
    path('delete-commission', views.delete_commission),
]
