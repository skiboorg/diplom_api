# Generated by Django 4.2 on 2023-04-19 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_alter_service_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_pay',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Оплачено'),
        ),
    ]