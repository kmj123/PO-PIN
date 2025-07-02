from django.db import models
from django.conf import settings

# 동행 카테고리 (콘서트, 팬미팅 등)
class CompanionCategory(models.TextChoices):
    CONCERT = '콘서트', '콘서트'
    FANSIGN = '팬사인회', '팬사인회'
    POPUP = '팝업스토어', '팝업스토어'
    EXHIBITION = '전시회', '전시회'
    GOODS = '굿즈샵', '굿즈샵'
    ETC = '기타', '기타'
# 태그  
class CompanionTag(models.Model):
    name = models.CharField("태그명", max_length=30, unique=True)

    def __str__(self):
        return self.name
    
# 동행 모집 게시글
class CompanionPost(models.Model):
    title = models.CharField("제목", max_length=100)
    content = models.TextField("본문")

    category = models.CharField("카테고리", max_length=20, choices=CompanionCategory.choices)
    artist = models.CharField("아티스트", max_length=50)

    event_date = models.DateTimeField("행사 날짜 및 시간")
    location = models.CharField("위치", max_length=100)

    max_people = models.PositiveIntegerField("최대 모집 인원")
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="joined_companions",
        verbose_name="참여자 목록"
    )

    status = models.CharField(
        "모집 상태",
        max_length=10,
        choices=[('모집중', '모집중'), ('모집완료', '모집완료'),('진행중', '진행중')],
        default='모집중'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="companion_posts",
        verbose_name="작성자"
    )

    created_at = models.DateTimeField("작성일", auto_now_add=True)
    views = models.PositiveIntegerField("조회수", default=0)
    comments_count = models.PositiveIntegerField("댓글 수", default=0)

    def __str__(self):
        return f"[{self.artist}] {self.title}"

    @property
    def current_people(self):
        return self.participants.count()

    @property
    def status_display_with_count(self):
        return f"{self.current_people}/{self.max_people} ({self.status})"

# 댓글 모델 (선택)
class CompanionComment(models.Model):
    post = models.ForeignKey(CompanionPost, on_delete=models.CASCADE, related_name="comments", verbose_name="게시글")
    content = models.TextField("댓글 내용")
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content[:20]}"
    
    
    
class CompanionImage(models.Model):
    post = models.ForeignKey(CompanionPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField("첨부 이미지", upload_to='companion_images/')
    caption = models.CharField("이미지 설명", max_length=100, blank=True)
    uploaded_at = models.DateTimeField("업로드 시간", auto_now_add=True)

    def __str__(self):
        return f"{self.post.title}의 이미지"