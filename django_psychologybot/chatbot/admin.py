from django.contrib import admin
from .models import Methodology
from .models import Report

@admin.register(Methodology)
class MethodologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'edited_at', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'military_number', 'language']
    readonly_fields = ('file', 'created_at', 'edited_at')
    list_display = ['full_name', 'military_number', 'language', 'created_at', 'edited_at']
    list_filter = ['language', 'created_at']
    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj)
