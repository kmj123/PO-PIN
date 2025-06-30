from django.contrib import admin
from .models import ProxyPost, ProxyComment
from .models import ProxyTag

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