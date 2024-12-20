import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .elasticsearch_utils import index_document, delete_document, get_tenant_index
from .models import Notifications
from django_tenants.utils import schema_context
from django.db import connection

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Notifications)
def handle_notification_save(sender, instance, created, **kwargs):
    if created:
        schema_name = connection.schema_name
        with schema_context(schema_name):  # Explicitly set schema context
            index_name = get_tenant_index(schema_name)
            print(f"Schema Name: {schema_name}, Index Name: {index_name}")
            document = {
                "message": instance.message,
                "created_at": instance.created_at.isoformat(),
                "read": instance.read,
            }
            logger.info(f"Indexing Document: {document} into Index: {index_name}")
            index_document(index_name, instance.id, document)


        # Handle WebSocket notifications
        channel_layer = get_channel_layer()
        group_name = f"notifications_{instance.user.id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "notification": {
                    "id": instance.id,
                    "message": instance.message,
                    "created_at": instance.created_at.isoformat(),
                    "read": instance.read,
                },
            },
        )


@receiver(post_delete, sender=Notifications)
def delete_notification(sender, instance, **kwargs):
    schema_name = instance._state.db
    index_name = get_tenant_index(schema_name)
    delete_document(index_name, instance.id)


# @receiver(post_save, sender=Notifications)
# def send_notification_on_save(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         with schema_context(instance._state.db):  # Ensure the correct tenant DB
#             group_name = f"notifications_{instance.user.id}"
#             async_to_sync(channel_layer.group_send)(
#                 group_name,
#                 {
#                     "type": "send_notification",
#                     "notification": {
#                         "id": instance.id,
#                         "message": instance.message,
#                         "created_at": instance.created_at.isoformat(),
#                         "read": instance.read,
#                     },
#                 },
#             )


# @receiver(post_save, sender=Notifications)
# def send_notification_to_group(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         group_name = f"notifications_{instance.user.id}"

#         async_to_sync(channel_layer.group_send)(
#             group_name,
#             {
#                 "type": "send_notification",
#                 "notification": {
#                     "id": instance.id,
#                     "message": instance.message,
#                     "created_at": instance.created_at.isoformat(),
#                     "read": instance.read,
#                 },
#             },
#         )
