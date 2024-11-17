# chat/consumers.py
from datetime import timezone
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        user_color = event.get('user_color', '#000000')  # Couleur par défaut

        # Envoyer les données au WebSocket
        await self.send(text_data=json.dumps({
            'message': {
                'value': message,
                'user': user,
                'user_color': user_color,
                'date': timezone.now().strftime('%H:%M:%S'),  # Exemple d'heure
            }
        }))