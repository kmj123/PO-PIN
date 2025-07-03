from django.contrib import admin
from .models import SharingPost, SharingTag, SharingImage
from django.forms import BaseInlineFormSet, ValidationError

@admin.register(SharingTag)
class SharingTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    
### 이미지 개수 제한용 FormSet
class LimitedImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_forms = len([
            form for form in self.forms
            if not form.cleaned_data.get('DELETE', False) and form.cleaned_data
        ])
        if self.instance.images.count() + total_forms > 5:
            raise ValidationError('이미지는 최대 5개까지만 등록할 수 있습니다.')



class SharingImageInline(admin.TabularInline):  # 이미지 인라인으로 등록
    model = SharingImage
    extra = 1
    readonly_fields = ['uploaded_at']
    formset = LimitedImageInlineFormSet

@admin.register(SharingPost)
class SharingPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'type', 'share_date', 'location', 'created_at', 'views']
    list_filter = ['category', 'type', 'share_date']
    search_fields = ['title', 'content', 'author__username', 'tags__name']
    readonly_fields = ['views', 'created_at']
    inlines = [SharingImageInline]
    filter_horizontal = ['tags']  # 태그 다중 선택 UI


@admin.register(SharingImage)
class SharingImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'uploaded_at']
    readonly_fields = ['uploaded_at']