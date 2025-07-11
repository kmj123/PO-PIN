# Generated by Django 5.2.1 on 2025-07-01 02:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='제목')),
                ('content', models.TextField(verbose_name='후기 내용')),
                ('artist', models.CharField(max_length=50, verbose_name='아티스트')),
                ('category', models.CharField(choices=[('앨범', '앨범'), ('굿즈', '굿즈'), ('기타', '기타')], max_length=20, verbose_name='카테고리')),
                ('method', models.CharField(choices=[('온라인', '온라인'), ('오프라인', '오프라인')], max_length=20, verbose_name='교환 방식')),
                ('overall_score', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='총 평점')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_reviews', to=settings.AUTH_USER_MODEL, verbose_name='교환 상대방')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='written_reviews', to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='review_images/', verbose_name='첨부 이미지')),
                ('caption', models.CharField(blank=True, max_length=100, verbose_name='이미지 설명')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='chgReview.exchangereview')),
            ],
        ),
    ]
