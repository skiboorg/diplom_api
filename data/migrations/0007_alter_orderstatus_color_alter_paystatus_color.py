# Generated by Django 4.2 on 2023-04-20 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_orderstatus_color_paystatus_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderstatus',
            name='color',
            field=models.CharField(max_length=255, null=True, verbose_name='Цвет (red - красный, green - зеленый, blue - синий, yellow - желтый)'),
        ),
        migrations.AlterField(
            model_name='paystatus',
            name='color',
            field=models.CharField(max_length=255, null=True, verbose_name='Цвет (red - красный, green - зеленый, blue - синий, yellow - желтый)'),
        ),
    ]
