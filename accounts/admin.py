from django.contrib import admin
from .models import SupabaseUser, UserProfile


@admin.register(SupabaseUser)
class SupabaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'supabase_id', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'supabase_id')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('email',)
    fieldsets = (
        ('User Info', {'fields': ('email', 'username', 'supabase_id', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'username', 'vehicle_name', 'vehicle_type', 'manufacturer')
    search_fields = ('email', 'username', 'name', 'vehicle_name', 'vehicle_type', 'manufacturer')
    list_filter = ('vehicle_type', 'manufacturer')
    ordering = ('email',)











