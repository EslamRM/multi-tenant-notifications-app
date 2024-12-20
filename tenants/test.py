from django.test import TestCase
from django_tenants.utils import schema_context, tenant_context
from tenants.models import Tenant, Domain
from django.contrib.auth import get_user_model

User = get_user_model()


class TenantModelTest(TestCase):
    def setUp(self):
        # Create tenants
        self.tenant1 = Tenant.objects.create(name="Tenant 1", schema_name="tenant1")
        self.tenant2 = Tenant.objects.create(name="Tenant 2", schema_name="tenant2")

        # Create domains
        self.domain1 = Domain.objects.create(
            tenant=self.tenant1, domain="tenant1.localhost"
        )
        self.domain2 = Domain.objects.create(
            tenant=self.tenant2, domain="tenant2.localhost"
        )

        # Create users and assign them to tenants
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.tenant1.users.add(self.user1)
        self.tenant2.users.add(self.user2)

    def test_tenant_creation(self):
        """Test tenant schema creation."""
        self.assertEqual(Tenant.objects.count(), 2)
        self.assertEqual(self.tenant1.name, "Tenant 1")
        self.assertEqual(self.tenant2.schema_name, "tenant2")

    def test_domain_association(self):
        """Test domain association with tenants."""
        self.assertEqual(self.domain1.tenant, self.tenant1)
        self.assertEqual(self.domain2.domain, "tenant2.localhost")

    def test_user_tenant_relationship(self):
        """Test user-to-tenant relationships."""
        self.assertIn(self.user1, self.tenant1.users.all())
        self.assertIn(self.user2, self.tenant2.users.all())
        self.assertEqual(self.user1.tenants.first(), self.tenant1)

    def test_string_representation(self):
        """Test the string representation of the Tenant model."""
        self.assertEqual(str(self.tenant1), "Tenant 1")
        self.assertEqual(str(self.tenant2), "Tenant 2")

    def test_domain_retrieval(self):
        """Test domain retrieval for a tenant."""
        self.assertEqual(self.tenant1.domains.first().domain, "tenant1.localhost")
        self.assertEqual(self.tenant2.domains.first().domain, "tenant2.localhost")
