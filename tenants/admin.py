from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django_tenants.admin import TenantAdminMixin
from django.db import connection
from django_tenants.utils import schema_context
from .models import Domain, Tenant


# Inline for managing domains associated with tenants
class DomainInline(admin.TabularInline):
    model = Domain
    max_num = 1  # Limit to one domain per tenant
    extra = 0  # Hide extra blank fields by default

    # Ensure unique domain names across tenants
    def save_model(self, request, obj, form, change):
        if Domain.objects.exclude(pk=obj.pk).filter(domain=obj.domain).exists():
            raise admin.ValidationError(f"The domain '{obj.domain}' is already in use.")
        super().save_model(request, obj, form, change)


# Custom admin for managing tenants
@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name", "created_on", "is_active")
    list_filter = ("created_on", "is_active")
    search_fields = ("name",)
    inlines = [DomainInline]

    # Restrict access to tenant model only for superusers and public schema
    def has_module_permission(self, request):
        return connection.schema_name == "public" and request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return connection.schema_name == "public" and request.user.is_superuser

    def has_add_permission(self, request):
        return connection.schema_name == "public" and request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return connection.schema_name == "public" and request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return connection.schema_name == "public" and request.user.is_superuser

    # Add custom actions
    actions = ["activate_tenants", "deactivate_tenants"]

    def activate_tenants(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected tenants have been activated.")

    activate_tenants.short_description = "Activate selected tenants"

    def deactivate_tenants(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected tenants have been deactivated.")

    deactivate_tenants.short_description = "Deactivate selected tenants"


# Custom admin for managing users within tenants
class TenantUserAdmin(UserAdmin):
    def get_queryset(self, request):
        with schema_context(connection.schema_name):
            return super().get_queryset(request)

    # Restrict actions based on the schema
    def has_module_permission(self, request):
        return (
            connection.schema_name != "public"
        )  # Hide user management in public schema


# Unregister the default User admin and re-register with custom admin
admin.site.unregister(User)
admin.site.register(User, TenantUserAdmin)
