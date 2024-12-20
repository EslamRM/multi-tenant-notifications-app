from django.contrib import admin
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notifications
from django_tenants.utils import schema_context


@admin.action(description="Send WebSocket notification")
def send_websocket_notification(modeladmin, request, queryset):
    channel_layer = get_channel_layer()
    for notification in queryset:
        tenant_schema = request.tenant.schema_name
        with schema_context(tenant_schema):
            group_name = f"notifications_{notification.user.id}"
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "send_notification",
                    "notification": {
                        "message": notification.message,
                        "timestamp": notification.created_at.isoformat(),
                        "read": notification.read,
                    },
                },
            )


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "user", "created_at", "read")
    actions = [send_websocket_notification]


admin.site.register(Notifications, NotificationAdmin)
