from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, StockOperation, Market, FuturesOperation, FuturesOptionsOperation, OperationChain, \
    Commissions, OperationCommission


class UserChangeFormCustom(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email', 'name', 'surnames', 'organization')


class UserCreationFormCustom(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'name', 'surnames', 'organization')


class UserAdmin(BaseUserAdmin):
    form = UserChangeFormCustom
    add_form = UserCreationFormCustom
    list_display = ('email', 'name', 'surnames', 'organization', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surnames', 'organization')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surnames', 'organization', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name', 'surnames')
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency')
    search_fields = ('name', 'currency')


@admin.register(StockOperation)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'type', 'date', 'market', 'trader', 'description', 'shares_amount', 'created_by', 'modified_by',
        'operation_chain')
    list_filter = ('date', 'market', 'trader', 'created_by', 'modified_by', 'operation_chain')
    search_fields = ('trader', 'description')


@admin.register(FuturesOperation)
class FutureAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'type', 'date', 'market', 'trader', 'description', 'contract', 'created_by', 'modified_by',
        'operation_chain')
    list_filter = ('date', 'market', 'trader', 'created_by', 'modified_by', 'operation_chain')
    search_fields = ('trader', 'description', 'contract')


@admin.register(FuturesOptionsOperation)
class OptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'type', 'date', 'market', 'trader', 'description', 'strike_price', 'created_by', 'modified_by',
        'operation_chain')
    list_filter = ('date', 'market', 'trader', 'strike_price', 'created_by', 'modified_by', 'operation_chain')
    search_fields = ('trader', 'description', 'strike_price')


@admin.register(OperationChain)
class OperationChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('id',)


@admin.register(Commissions)
class OperationsCommissionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'modified_by')
    search_fields = ('name', 'created_by__email', 'modified_by__email')
    list_filter = ('created_by', 'modified_by')
    readonly_fields = ('id',)


@admin.register(OperationCommission)
class OperationCommissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'operation', 'commission', 'amount')
    search_fields = ('operation__id', 'commission__name', 'amount')
    list_filter = ('operation', 'commission')
    readonly_fields = ('id',)


admin.site.register(User, UserAdmin)
