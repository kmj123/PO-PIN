from django.contrib import admin
from .models import ExchangeReview, ReviewImage, ReviewTag

class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1

@admin.register(ExchangeReview)
class ExchangeReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "writer", "partner", "overall_score", "created_at", "views")
    list_filter = ("category", "method", "created_at")
    search_fields = ("title", "content", "writer__username", "partner__username")
    inlines = [ReviewImageInline]
    filter_horizontal = ("tags",)

@admin.register(ReviewTag)
class ReviewTagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ("review", "image", "caption")  #  'uploaded_at' 제거
    readonly_fields = ("uploaded_at",)  #  필요 없으면 주석처리하거나 삭제