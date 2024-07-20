from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, StockOperation, Market, FuturesOperation, FuturesOptionsOperation


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
    list_display = ('id', 'date', 'market', 'trader', 'description', 'shares_amount', 'created_by', 'modified_by', 'operation_chain')
    list_filter = ('date', 'market', 'trader', 'created_by', 'modified_by', 'operation_chain')
    search_fields = ('trader', 'description')

@admin.register(FuturesOperation)
class FutureAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'market', 'trader', 'description', 'contract', 'created_by', 'modified_by', 'operation_chain')
    list_filter = ('date', 'market', 'trader', 'created_by', 'modified_by', 'operation_chain')
    search_fields = ('trader', 'description', 'contract')

@admin.register(FuturesOptionsOperation)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'market', 'trader', 'description', 'strike_price', 'created_by', 'modified_by', 'operation_chain')
    list_filter = ('date', 'market', 'trader', 'strike_price', 'created_by', 'modified_by', 'operation_chain')
    search_fields = ('trader', 'description', 'strike_price')


admin.site.register(User, UserAdmin)
