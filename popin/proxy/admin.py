from django.contrib import admin
from .models import ProxyPost, ProxyComment
from .models import ProxyTag
from .models import ProxyImage
from django.forms import BaseInlineFormSet, ValidationError
# 최대 5장 제한용 FormSet
class LimitedImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_forms = len([
            form for form in self.forms
            if not form.cleaned_data.get('DELETE', False) and form.cleaned_data
        ])
        if self.instance.images.count() + total_forms > 5:
            raise ValidationError('이미지는 최대 5개까지만 등록할 수 있습니다.')
# 이미지 인라인
class ProxyImageInline(admin.TabularInline):
    model = ProxyImage
    extra = 1
    formset = LimitedImageInlineFormSet
    readonly_fields = ['uploaded_at']
    from .models import ProxyImage

@admin.register(ProxyImage)
class ProxyImageAdmin(admin.ModelAdmin):
    list_display = ("post", "image", "caption", "uploaded_at")
    readonly_fields = ("uploaded_at",)
    
#태그
@admin.register(ProxyTag)
class ProxyTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(ProxyPost)
class ProxyPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category', 'status', 'author', 'created_at', 'views')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title', 'artist', 'description', 'location')
    readonly_fields = ('created_at', 'views', 'comments_count')

@admin.register(ProxyComment)
class ProxyCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at',)