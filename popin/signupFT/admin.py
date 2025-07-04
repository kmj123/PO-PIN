from django.contrib import admin
from .models import User, UserRelation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'nickname', 'email', 'state', 'created_at')
    list_filter = ('state', 'gender', 'created_at')
    search_fields = ('user_id', 'username', 'nickname', 'email')
    ordering = ('-created_at',)

@admin.register(UserRelation)
class UserRelationAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'relation_type')
    search_fields = ('from_user__nickname', 'to_user__nickname')