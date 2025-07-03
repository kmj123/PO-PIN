from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from idols.models import Group, Member

# 선택지 정의
GENDER_CHOICES = [
    ('M', '남성'),
    ('F', '여성'),
]

USER_STATE_CHOICES = [
    (0, '관리자'),
    (1, '일반 사용자'),
    (2, '숨김 사용자'),
    (3, '차단된 사용자'),
]

class User(AbstractUser):
    # Django 기본 필드: username, password, email 등 이미 포함됨
    user_id = models.CharField(max_length=50, unique=True, verbose_name="사용자 ID")  # primary_key❌ → unique✅
    name = models.CharField(max_length=100, verbose_name="이름")
    birth_date = models.DateField(null=True, blank=True, verbose_name="생년월일")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name="성별")
    email = models.EmailField(unique=True, verbose_name="이메일")
    reported_by = models.TextField(default="", blank=True, verbose_name="신고당한 횟수")
    
    bias_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name='fans_group',
        verbose_name="최애 그룹"
    )
    
    bias_member = models.ManyToManyField(
        Member,
        blank=True,
        related_name='fans_member',
        verbose_name="최애 멤버"
    )

    phone = models.CharField(max_length=20, blank=True, default='', verbose_name="전화번호")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="주소")
    state = models.IntegerField(choices=USER_STATE_CHOICES, default=1, verbose_name="사용자 상태")
    manners_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name="매너 온도"
    )
    nickname = models.CharField(max_length=100, unique=True, verbose_name="닉네임")
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name="프로필 이미지")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="가입일")
    agree_marketing = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="최근 수정일")

    # ✅ AbstractUser 필수 설정
    USERNAME_FIELD = 'username'  # 기본 필드 사용
    REQUIRED_FIELDS = ['email']  # createsuperuser 시 필수

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nickname} ({self.user_id})"


class UserRelation(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_relations',
        verbose_name="관계 시작 사용자"
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_relations',
        verbose_name="관계 대상 사용자"
    )
    RELATION_CHOICES = [
        ('FOLLOW', '관심 사용자'),
        ('BLOCK', '차단한 사용자'),
    ]
    relation_type = models.CharField(
        max_length=10,
        choices=RELATION_CHOICES,
        verbose_name="관계 유형"
    )

    class Meta:
        unique_together = ('from_user', 'to_user', 'relation_type')
        verbose_name = "사용자 관계"
        verbose_name_plural = "사용자 관계 목록"

    def __str__(self):
        return f"{self.from_user.user_id}가 {self.to_user.user_id}를 {self.get_relation_type_display()}"