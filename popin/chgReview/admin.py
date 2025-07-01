from django.contrib import admin
from .models import ExchangeReview, ReviewImage, ReviewTag

# 이미지 인라인
class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1

# 후기 리뷰 어드민
@admin.register(ExchangeReview)
class ExchangeReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "writer", "partner", "overall_score", "method", "created_at", "views")
    list_filter = ("method", "created_at")
    search_fields = ("title", "content", "writer__username", "partner__username", "artist")
    inlines = [ReviewImageInline]
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at", "views")

# 태그 어드민
@admin.register(ReviewTag)
class ReviewTagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# 이미지 어드민
@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ("review", "image", "caption")
    readonly_fields = ("uploaded_at",)