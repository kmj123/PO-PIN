from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # URL에서 채팅방 id(room_name)를 가져옴
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 그룹에 현재 WebSocket 연결 추가
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # 연결 수락
        self.accept()

    def disconnect(self, code):
        # 그룹에서 연결 제거
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        import json
        from .models import ChatMessage, ChatRoom, User  # 🔁 모델 import (지연 로딩 방식)

        data = json.loads(text_data)
        message = data.get('message', '').strip()

        # 세션에서 user_id 추출
        session = self.scope.get("session")
        user_id = session.get("user_id") if session else None

        if not user_id:
            self.close()
            return

        # 사용자 조회
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            self.close()
            return

        # 채팅방 조회
        try:
            room = ChatRoom.objects.get(id=self.room_name)
        except ChatRoom.DoesNotExist:
            self.close()
            return

        # 메시지 저장
        chat = ChatMessage.objects.create(
            room=room,
            send_user=user,
            message=message
        )

        # 동일 그룹에 메시지 전송
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': chat.message,
                'user_id': user.user_id,
                'timestamp': chat.timestamp.strftime("%p %I:%M")
                                     .replace("AM", "오전")
                                     .replace("PM", "오후"),
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
            'user_id': event['user_id'],
            'timestamp': event['timestamp'],
        }))
