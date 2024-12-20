import logging
from django.test import TestCase
from django.contrib.auth import get_user_model
from tenants.models import Tenant
from django_tenants.utils import schema_context
from notifications.models import Notifications
from notifications.serializers import NotificationSerializer

logger = logging.getLogger(__name__)


class NotificationsModelTest(TestCase):
    def setUp(self):
        logger.info("Setting up test data for NotificationsModelTest.")
        # Create tenant and set schema context
        self.tenant = Tenant.objects.create(
            name="Test Tenant", schema_name="test_tenant"
        )
        with schema_context(self.tenant.schema_name):
            self.user = get_user_model().objects.create_user(
                username="testuser", password="password"
            )
            self.notification = Notifications.objects.create(
                user=self.user, message="Test notification"
            )

    def test_notification_creation(self):
        with schema_context(self.tenant.schema_name):
            logger.info("Testing notification creation.")
            self.assertEqual(
                str(self.notification),
                f"Notification for {self.user.username}: Test notification",
            )
            self.assertFalse(self.notification.read)
            logger.info("Notification creation test passed.")


class NotificationSerializerTest(TestCase):
    def setUp(self):
        logger.info("Setting up test data for NotificationSerializerTest.")
        # Create tenant and set schema context
        self.tenant = Tenant.objects.create(
            name="Test Tenant", schema_name="test_tenant"
        )
        with schema_context(self.tenant.schema_name):
            self.user = get_user_model().objects.create_user(
                username="testuser", password="password"
            )
            self.notification = Notifications.objects.create(
                user=self.user, message="Test notification"
            )

    def test_notification_serializer(self):
        with schema_context(self.tenant.schema_name):
            logger.info("Testing NotificationSerializer.")
            serializer = NotificationSerializer(self.notification)
            self.assertEqual(serializer.data["message"], "Test notification")
            self.assertFalse(serializer.data["read"])
            logger.info("NotificationSerializer test passed.")
