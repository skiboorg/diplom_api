# Generated by Django 4.2 on 2023-04-20 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_alter_order_total_pay'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderfile',
            old_name='user',
            new_name='order',
        ),
    ]