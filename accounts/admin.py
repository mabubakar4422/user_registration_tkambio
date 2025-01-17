from django.contrib import admin
from .models import Company

# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('legal_name', 'email', 'phone', 'state', 'city', 'created_at')
    list_filter = ('state', 'company_type', 'created_at')
    search_fields = ('legal_name', 'commercial_name', 'email', 'tax_id')
    date_hierarchy = 'created_at'
