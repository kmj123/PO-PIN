from django.contrib import admin
from .models import SharingPost, SharingTag, SharingImage

@admin.register(SharingTag)
class SharingTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class SharingImageInline(admin.TabularInline):  # 이미지 인라인으로 등록
    model = SharingImage
    extra = 1
    readonly_fields = ['uploaded_at']


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