# Generated by Django 3.2.2 on 2021-05-07 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='receiver',
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_message', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chat',
            name='my_files',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='chat.attachment'),
        ),
    ]