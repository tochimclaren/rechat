from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


class Attachment(models.Model):
    attachment = models.FileField(blank=True, null=True, upload_to='media/user/attachments/', max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created

class Chat(models.Model):
    my_files = models.ForeignKey(Attachment, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_message')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    text = models.TextField(max_length=300)


    def __str__(self):
        if self.updated:
            return f'{self.created}. last updated: {self.updated}'
        return self.created

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name='friend_list')
    added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile_signals(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()

        print(f'Profile for this user {instance} was created')
