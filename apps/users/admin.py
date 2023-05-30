from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Define a new User admin
    """
    model = User
    list_display = ('email', 'username', 'first_name',
                    'last_name', 'is_staff')
    list_filter = ('is_staff', 'groups')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('username','first_name', 'last_name','infojobs_id')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # Agregamos los campos personalizados
        
    )


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)





