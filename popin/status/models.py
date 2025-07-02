from django.db import models
from django.conf import settings

class StatusPost(models.Model):
    CATEGORY_CHOICES = [
        ("콘서트", "콘서트"),
        ("팝업스토어", "팝업스토어"),
        ("팬사인회", "팬사인회"),
        ("전시회", "전시회"),
        ("굿즈샵", "굿즈샵"),
        ("기타", "기타"),
    ]

    REGION_CHOICES = [
        ("서울", "서울"),
        ("경기", "경기"),
        ("부산", "부산"),
        ("대구", "대구"),
        ("인천", "인천"),
        ("기타", "기타"),
    ]

    title = models.CharField("제목", max_length=200)
    content = models.TextField("본문 내용")
    category = models.CharField("카테고리", max_length=20, choices=CATEGORY_CHOICES)
    artist = models.CharField("아티스트", max_length=50)
    region = models.CharField("지역", max_length=20, choices=REGION_CHOICES)
    place = models.CharField("장소", max_length=200)
    event_datetime = models.DateTimeField("이벤트 일시")
    images = models.TextField("이미지 URL 목록", blank=True, help_text="쉼표로 구분된 이미지 URL 문자열")
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='status_posts',
        verbose_name="작성자"
    )
    views = models.PositiveIntegerField("조회수", default=0)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "현황 공유"
        verbose_name_plural = "현황 공유"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.artist}"