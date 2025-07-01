from django.db import models

class Board(models.Model):
    TYPE_CHOICES = [
        ('exchange-review', '교환후기'),
        ('offline-sharing', '나눔'),
        ('offline-proxy', '대리구매'),
        ('offline-status', '현황 공유'),
        ('offline-companion', '동행'),
        ('recent-activity', '최근 활동'),
    ]
    board_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=10, default='⭐')
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    description = models.TextField()
    features = models.TextField(help_text="특징 리스트를 줄바꿈으로 구분")
    stat_total = models.CharField(max_length=50)
    stat_label_total = models.CharField(max_length=50)
    stat_secondary = models.CharField(max_length=50, blank=True, null=True)
    stat_label_secondary = models.CharField(max_length=50, blank=True, null=True)
    stat_tertiary = models.CharField(max_length=50, blank=True, null=True)
    stat_label_tertiary = models.CharField(max_length=50, blank=True, null=True)
    write_url = models.URLField(blank=True, null=True)
    view_url = models.URLField(blank=True, null=True)

    def feature_list(self):
        return self.features.split('\n')

    def stats(self):
        stats = []
        if self.stat_total and self.stat_label_total:
            stats.append({'number': self.stat_total, 'label': self.stat_label_total})
        if self.stat_secondary and self.stat_label_secondary:
            stats.append({'number': self.stat_secondary, 'label': self.stat_label_secondary})
        if self.stat_tertiary and self.stat_label_tertiary:
            stats.append({'number': self.stat_tertiary, 'label': self.stat_label_tertiary})
        return stats

    def __str__(self):
        return self.title