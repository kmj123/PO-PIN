from django.db import models
from django.conf import settings

# 후기 태그
class ReviewTag(models.Model):
    name = models.CharField("태그명", max_length=30, unique=True)

    def __str__(self):
        return self.name

# 후기 모델
class ExchangeReview(models.Model):
    title = models.CharField("제목", max_length=100)
    content = models.TextField("후기 내용")
    
    # 작성자와 교환 상대방
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="written_reviews", verbose_name="작성자")
    partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_reviews", verbose_name="교환 상대방")

    tags = models.ManyToManyField(ReviewTag, blank=True, related_name="reviews", verbose_name="태그")
    artist = models.CharField("아티스트", max_length=50,default="기타")
    method = models.CharField("교환 방식", max_length=20, choices=[("온라인", "온라인"), ("오프라인", "오프라인")])
    transaction_type = models.CharField("거래 방식", max_length=10, choices=[("교환", "교환"), ("양도", "양도")], default="교환")

    overall_score = models.PositiveSmallIntegerField("총 평점 (1~5)", choices=[(i, f"{i}점") for i in range(1, 6)])

    created_at = models.DateTimeField("작성일", auto_now_add=True)
    views = models.PositiveIntegerField("조회수", default=0)

    def __str__(self):
        return f"[{self.title}] {self.writer} → {self.partner}"

# 이미지
class ReviewImage(models.Model):
    review = models.ForeignKey(ExchangeReview, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField("첨부 이미지", upload_to='review_images/')
    caption = models.CharField("이미지 설명", max_length=100, blank=True)
    uploaded_at = models.DateTimeField("업로드 시간", auto_now_add=True)

    def __str__(self):
        return f"Image for {self.review.title}"