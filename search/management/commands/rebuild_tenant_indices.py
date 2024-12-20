from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model, schema_context
from django.core.management import call_command


class Command(BaseCommand):
    help = "Rebuild Elasticsearch indices for all tenants"

    def handle(self, *args, **kwargs):
        TenantModel = get_tenant_model()
        tenants = TenantModel.objects.all()
        for tenant in tenants:
            schema_info = schema_context(tenant.schema_name)
            if schema_info:
                with schema_context(tenant.schema_name):
                    self.stdout.write(f"Rebuilding index for tenant: {tenant.schema_name}")
                    call_command("search_index", "--rebuild")
