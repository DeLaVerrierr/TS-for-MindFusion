from django.db import models

class UserProfile(models.Model):
    chat_id = models.IntegerField(unique=True)
    user_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, default='', null=True)
    last_name = models.CharField(max_length=50, default='', null=True)
    time = models.DateTimeField()
    choice = models.CharField(max_length=50, default='',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Character(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='characters')

    def __str__(self):
        return self.name


class DialogMessage(models.Model):
    user_id = models.IntegerField()
    character_name = models.CharField(max_length=100)
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.character_name} to {self.user_id}: {self.message_text}'
