from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "f_name", "l_name", "is_admin"]
    search_fields = ["email"]
    ordering = ["email"]
    list_filter = ["is_admin"]
    filter_horizontal = []


admin.site.unregister(Group)

