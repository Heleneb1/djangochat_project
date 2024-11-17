import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = data['user']
        user_color = data.get('user_color', '#000')  # Couleur par défaut

        # Formater un message
        formatted_message = {
            'message': {
                'user': user,
                'value': message,
                'user_color': user_color,
                'date': datetime.now().strftime("%H:%M:%S"),
            }
        }

        # Envoyer le message à tous les clients du groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': formatted_message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps(message))

