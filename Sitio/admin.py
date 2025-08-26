from django.contrib import admin
from .models import UserCredential

@admin.register(UserCredential)
class UserCredentialAdmin(admin.ModelAdmin):
    list_display = ('email', 'github_connected', 'github_username', 'created_at')
    list_filter = ('github_connected', 'created_at')
    search_fields = ('email', 'github_username')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('email', 'password')
        }),
        ('GitHub', {
            'fields': ('github_connected', 'github_username')
        }),
        ('Fechas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
