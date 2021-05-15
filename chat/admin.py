from django.contrib import admin
from .models import Chat, Profile


class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender', 'user', 'created', 'updated']


admin.site.register(Chat, ChatAdmin)


class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)