# Generated by Django 4.2 on 2023-04-27 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_user_comment_usercomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercomment',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
