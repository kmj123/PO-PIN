from django.contrib import admin
from .models import ExchangeReview, ReviewImage, ReviewTag
from django.forms import BaseInlineFormSet, ValidationError
### 이미지 개수 제한용 FormSet
class LimitedImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_forms = len([
            form for form in self.forms
            if not form.cleaned_data.get('DELETE', False) and form.cleaned_data
        ])
        #  pk 존재할 때만 이미지 개수 체크
        if self.instance.pk and self.instance.images.count() + total_forms > 5:
            raise ValidationError('이미지는 최대 5개까지만 등록할 수 있습니다.')

# 이미지 인라인
class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1
    readonly_fields = ['uploaded_at']
    formset = LimitedImageInlineFormSet
    
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