from django.contrib import admin
from django.utils.html import format_html

from .models import UserData


def mark_as_old(modeladmin, request, queryset):
    for data in queryset:
        data.status = UserData.OLD
        data.save()


class UserDataAdmin(admin.ModelAdmin):
    list_display = ['map_link', 'id', 'ip_address', 'user_agent', 'address', 'location', 'map', 'timestamp']
    actions = [mark_as_old, ]

    def map_link(self, user):
        return format_html("<a href='{url}/maps/{user_id}/' target='_blank'>View Map</a>", url="", user_id=user.id)


mark_as_old.short_description = 'Mark selected data as old'
admin.site.register(UserData, UserDataAdmin)
