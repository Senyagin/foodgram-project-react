from django.contrib import admin
from django.contrib.admin import register

from .models import Follow, User


@register(User)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'password'
    )
    list_filter = (
        'first_name',
        'email',
    )


@register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'user',
    )
    search_fields = (
        'user',
        'author',
    )
    list_per_page = 20
