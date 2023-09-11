from django.contrib import admin
from .models import UserProfile, Character, DialogMessage

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user_name', 'first_name', 'last_name', 'time', 'choice')

admin.site.register(UserProfile, UserProfileAdmin)

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'photo')

admin.site.register(Character, CharacterAdmin)

class DialogMessageAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'character_name', 'message_text', 'timestamp')

admin.site.register(DialogMessage, DialogMessageAdmin)
