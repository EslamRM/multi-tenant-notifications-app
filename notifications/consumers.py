# notifications/consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join a group for the logged-in user
        self.group_name = f"notifications_{self.scope['user'].id}"

        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive messages from the group
    async def receive(self, text_data):
        if not text_data:
            logger.error("Received empty message")
            return

        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", "No message content")
            logger.info(f"Parsed message: {message}")

            # Broadcast the message
            await self.channel_layer.group_send(
                "notifications",
                {
                    "type": "send_notification",
                    "message": message,
                },
            )
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}. Received data: {text_data}")

    async def send_notification(self, event):
        # Send message to WebSocket
        message = event["notification"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )
