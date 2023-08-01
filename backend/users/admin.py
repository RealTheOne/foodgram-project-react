from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

EMPTY_VALUE = '-empty-'


@admin.register(User)
class UserAdmin(UserAdmin):
    """User administrator."""

    list_display = ('id', 'username', 'email', 'first_name', 'last_name',)
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email',)
    empty_value_display = EMPTY_VALUE
