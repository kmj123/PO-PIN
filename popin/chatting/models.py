from django.db import models
from signupFT.models import User

CATEGORY_CHOICES = [
        ('exchange', '교환'),
        ('sale', '판매'),
        ('proxy', '대리구매'),
        ('companion', '동행'),
        ('inquiry', '문의'),
    ]

class ChatRoom(models.Model):
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES) # 교환, 판매, 동행, 대리구매, 문의
    post_id = models.CharField(max_length=255) # pno, 교환과 커뮤니티의 모델 구조가 다르기에 참조할 수 없어 pno만 지정
    host_user = models.ForeignKey(User, related_name='rooms_as_host', on_delete=models.CASCADE) # 글 작성자, (문의: 관리자)
    guest_user = models.ForeignKey(User, related_name='rooms_as_guest', on_delete=models.CASCADE) # 참여자 (구매자, 댈구 참여, 동행 희망자, 문의 사용자)
    created_at = models.DateTimeField(auto_now_add=True) # 생성일자
    last_message = models.TextField(null=True, blank=True) # 해당 룸 마지막 메시지
    last_timestamp = models.DateTimeField(null=True, blank=True) # 해당 룸 마지막 메시지 전송 시각

    def __str__(self):
        return f"{self.category}-{self.post_id} ({self.host_user} ↔ {self.guest_user})"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', default=1) # ChatRoom
    send_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages') # 메시지 보낸 유저
    message = models.TextField(blank=True) # 메시지 텍스트 내용
    file = models.FileField(upload_to='chat_images/', null=True, blank=True) # 이미지 메시지 (message | image 택 1)
    timestamp = models.DateTimeField(auto_now_add=True) # 보낸 시각
    is_read = models.BooleanField(default=False) # 메시지 수신자가 이 메시지를 읽었는가 (읽었으면 True)

    def __str__(self):
        return f"{self.send_user} → {self.message[:10] or self.file.name}"