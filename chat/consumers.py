# chat/consumers.py
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
        print(f"✅ WebSocket connecté: room={self.room_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"❌ WebSocket déconnecté: room={self.room_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = data['user']
        user_color = data.get('user_color', '#000')
        
        print(f"📨 Message reçu: {user}: {message}")
        
        # Envoyer le message à tous les clients du groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {  # ✅ Une seule couche 'message'
                    'user': user,
                    'value': message,
                    'user_color': user_color,
                    'date': datetime.now().strftime("%H:%M:%S"),
                }
            }
        )

    async def chat_message(self, event):
        # ✅ Envoyer directement event (qui contient déjà 'message')
        await self.send(text_data=json.dumps(event))