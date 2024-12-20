from django.core.management.base import BaseCommand
from tenants.models import Tenant
from notifications.utils import create_index_for_tenant


class Command(BaseCommand):
    help = "Rebuild Elasticsearch indices for all tenants"

    def handle(self, *args, **kwargs):
        for tenant in Tenant.objects.all():
            create_index_for_tenant(tenant.schema_name)
            self.stdout.write(f"Rebuilt index for tenant: {tenant.schema_name}")
