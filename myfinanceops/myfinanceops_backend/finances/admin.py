from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from finances.models import User, OperationChain, Market, StockOperation, FuturesOperation, FuturesOptionsOperation


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'name', 'surnames', 'organization')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ['email', 'name', 'surnames', 'organization']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surnames', 'organization')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'surnames', 'organization'),
        }),
    )
    ordering = ('email',)  # Corrected to use 'email' instead of 'username'

    class StockOperationAdmin(admin.ModelAdmin):
        list_display = ('id', 'date', 'market', 'trader', 'description', 'operation_chain')

    class FuturesOperationAdmin(admin.ModelAdmin):
        list_display = ('id', 'date', 'market', 'trader', 'description', 'operation_chain')

    class FuturesOptionsOperationAdmin(admin.ModelAdmin):
        list_display = ('id', 'date', 'market', 'trader', 'description', 'operation_chain')

    class MarketAdmin(admin.ModelAdmin):
        list_display = ('name', 'currency')

    class OperationChainAdmin(admin.ModelAdmin):
        list_display = ('id', 'created_at')

    # Register your models here
    admin.site.register(StockOperation, StockOperationAdmin)
    admin.site.register(FuturesOperation, FuturesOperationAdmin)
    admin.site.register(FuturesOptionsOperation, FuturesOptionsOperationAdmin)
    admin.site.register(Market, MarketAdmin)
    admin.site.register(OperationChain, OperationChainAdmin)


admin.site.register(User, CustomUserAdmin)
