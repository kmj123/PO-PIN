from django.db import models
from django.conf import settings
from datetime import date

class TempUser(models.Model):
    user_id = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.user_id}'

class TempIdol(models.Model):
    group = models.CharField(max_length=50)
    member = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.group} | {self.member}'

    
class Photocard(models.Model):
    CATEGORY_CHOICES = [
        ('앨범', '앨범'),
        ('특전', '특전'),
        ('MD', 'MD'),
        ('공방', '공방'),
        ('기타', '기타'),
        # 필요시 추가
    ]

    P_STATE_CHOICES = [
        ('상', '상'),
        ('중', '중'),
        ('하', '하'),
    ]

    TRADE_CHOICES = [
        ('교환', '교환'),
        ('구매', '구매'),
    ]

    PLACE_CHOICES = [
        ('올림픽공원', '올림픽공원'),
        ('상암', '상암'),
        ('더현대', '더현대'),
        ('고척', '고척'),
        ('인스파이어', '인스파이어'),
        ('홍대', '홍대'),
    ]

    TRADE_STATE_CHOICES = [
        ('전', '거래전'),
        ('중', '거래중'),
        ('후', '거래완료'),
    ]
    
    # models.py

    pno = models.AutoField(primary_key=True)
    seller = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name='selling_photocards')
    buyer = models.ForeignKey(TempUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='buying_photocards')

    title = models.CharField(max_length=100, default='title')
    image = models.ImageField(upload_to='photocards/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Album')
    album = models.CharField(max_length=50, default='1집')
    idol = models.ForeignKey(TempIdol, on_delete=models.CASCADE, related_name='photocards')

    poca_state = models.CharField(max_length=20, choices=P_STATE_CHOICES, default='상')
    tag = models.CharField(max_length=20, null=True, blank=True)  # choices 생략됨
    trade_type = models.CharField(max_length=20, choices=TRADE_CHOICES, null=True)
    place = models.CharField(max_length=20, choices=PLACE_CHOICES, null=True)

    sell_state = models.CharField(max_length=20, choices=TRADE_STATE_CHOICES, default='전')
    buy_state = models.CharField(max_length=20, choices=TRADE_STATE_CHOICES, null=True, blank=True)

    hit = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    available_at = models.DateField(null=True, default=date.today)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.title} ({self.idol.group}/{self.idol.member})'

class TempWish(models.Model):
    user = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name='wished_photocards')
    photocard = models.ForeignKey(Photocard, on_delete=models.CASCADE, related_name='wished_by_users')
    
    def __str__(self):
        return f'{self.user.user_id} | {self.photocard.pno}'