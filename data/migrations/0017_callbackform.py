# Generated by Django 4.2.2 on 2023-08-09 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0016_category_short_text_category_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallbackForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(max_length=255, null=True)),
                ('time_to_call', models.CharField(max_length=255, null=True)),
                ('comment', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.service')),
            ],
        ),
    ]
