from django.urls import path, re_path
from finances import views
from finances.views import CreateOperationView, OperationsView, HomeView, OperationTypesView, get_operation_fields, \
    UpdateOperationView, add_commission, delete_commission, country_choices, create_trading_company, \
    delete_trading_company

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test-token', views.test_token),
    re_path('logout', views.logout),
    path('home', HomeView.as_view(), name='home'),
    path('create-operation', CreateOperationView.as_view(), name='create_operation'),
    path('update-operation', UpdateOperationView.as_view(), name='update_operation'),
    path('delete-operation/', views.delete_operation, name='delete_operation'),
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
    path('add-commission-to-operation/', views.add_commission, name='add_commission'),
    path('delete-commission-from-operation/', views.delete_commission, name='delete_commission'),
    path('country-choices/', views.country_choices, name='country-choices'),
    path('get-trading-companies', views.get_trading_companies),
    path('create-trading-company', create_trading_company, name='create_trading_company'),
    path('delete-trading-company', delete_trading_company, name='delete_trading_company'),
    path('get-trading-accounts', views.get_trading_accounts, name='get_trading_accounts'),
    path('add-trading-account', views.create_trading_account, name='add_trading_account'),
    path('delete-trading-account', views.delete_trading_account, name='delete_trading_account'),
    path('currency-choices', views.get_currency_choices, name='currency_choices'),

]
