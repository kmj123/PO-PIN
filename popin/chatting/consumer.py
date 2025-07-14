from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # URL에서 채팅방 이름을 가져와 변수에 저장
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # 채팅방 그룹 이름 설정 (채널 레이어 그룹 이름으로 사용됨)
        self.room_group_name = 'chat_%s' % self.room_name

        # 현재 WebSocket 연결을 그룹에 추가
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name  # 이 연결 고유의 채널 이름
        )

        # WebSocket 연결 수락
        self.accept()

    def disconnect(self, code):
        # 연결이 끊어질 때 그룹에서 현재 연결 제거
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # models import (여기서 하면 순환참조 피하기 쉬움)
        from .models import ChatMessage, User

        # 클라이언트로부터 수신된 JSON 문자열을 파싱
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 세션에서 user_id 가져오기 (로그인된 사용자 확인용)
        session = self.scope.get("session", None)
        user_id = session.get("user_id") if session else None

        # user_id 없으면 WebSocket 연결 종료
        if not user_id:
            self.close()
            return

        # user_id로 User 객체 조회 (존재하지 않으면 종료)
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            self.close()
            return

        # 채팅 메시지를 DB에 저장
        chat = ChatMessage.objects.create(
            room_id=self.room_name,
            message=message,
            user=user
        )

        # 저장한 메시지를 동일 방에 있는 다른 클라이언트들에게 전송
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',  # 아래의 chat_message 메서드가 호출됨
                'message': chat.message,
                'user_id':  chat.user.user_id,
                'timestamp': chat.timestamp.strftime("%p %I:%M")  # 시간 포맷 변환 (오전/오후 hh:mm)
                             .replace("AM", "오전")
                             .replace("PM", "오후"),
            }
        )

    # group_send로부터 전달된 메시지를 클라이언트에 직접 전송
    def chat_message(self, event):
        message = event['message']
        user_id = event.get('user_id', '')
        timestamp = event['timestamp']

        # 클라이언트에게 메시지 전송 (JSON 형식)
        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'timestamp': timestamp,
        }))
