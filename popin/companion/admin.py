from django.contrib import admin
from .models import CompanionPost, CompanionComment
from .models import CompanionTag
from .models import CompanionImage
from django.forms import BaseInlineFormSet, ValidationError

### 이미지 개수 제한용 FormSet
class LimitedImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_forms = len([form for form in self.forms if not form.cleaned_data.get('DELETE', False) and form.cleaned_data])
        if self.instance.images.count() + total_forms > 5:
            raise ValidationError('이미지는 최대 5개까지만 등록할 수 있습니다.')
        
# 이미지 인라인
class CompanionImageInline(admin.TabularInline):
    model = CompanionImage
    extra = 1
    readonly_fields = ['uploaded_at']
    formset = LimitedImageInlineFormSet

@admin.register(CompanionImage)
class CompanionImageAdmin(admin.ModelAdmin):
    list_display = ("post", "image", "caption", "uploaded_at")
    readonly_fields = ("uploaded_at",)
    
@admin.register(CompanionTag)
class CompanionTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(CompanionPost)
class CompanionPostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'artist',
        'category',
        'event_date',
        'location',
        'max_people',
        'status',
        'created_at',
        'views',
    )
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title', 'content', 'artist', 'location', 'author__username')
    autocomplete_fields = ('author', 'participants')
    readonly_fields = ('created_at', 'views')

@admin.register(CompanionComment)
class CompanionCommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'content',
        'created_at',
    )
    search_fields = ('post__title', 'content')
    autocomplete_fields = ["post"]  
    readonly_fields = ('created_at',)