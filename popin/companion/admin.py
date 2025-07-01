from django.contrib import admin
from .models import CompanionPost, CompanionComment
from .models import CompanionTag

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
        'author',
        'content',
        'created_at',
    )
    search_fields = ('post__title', 'author__username', 'content')
    autocomplete_fields = ('post', 'author')
    readonly_fields = ('created_at',)