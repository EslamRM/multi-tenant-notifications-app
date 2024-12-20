from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import User
from django.db import models


class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="tenants")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    auto_create_schema = True
    auto_drop_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass
