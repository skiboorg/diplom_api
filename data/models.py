from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import uuid

class Category(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)

    def __str__(self):
        return f'{self.name}'

class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=True,related_name='services')
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class PayStatus(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    color = models.CharField('Цвет (red - красный, green - зеленый, blue - синий, yellow - желтый)',
                             max_length=255, blank=False, null=True)

    def __str__(self):
        return f'{self.name}'

class OrderStatus(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    color = models.CharField('Цвет (red - красный, green - зеленый, blue - синий, yellow - желтый)',
                             max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=False, null=True)
    pay_status = models.ForeignKey(PayStatus, on_delete=models.SET_NULL, blank=True, default=1, null=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, blank=True, default=1, null=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=False, null=True,related_name='created_by')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=False, null=True,related_name='user')
    start_price = models.DecimalField('цена первоначальная', decimal_places=2, max_digits=10, blank=False, null=True)
    total_price = models.DecimalField('цена итоговая', decimal_places=2, max_digits=10, blank=True, null=True)
    start_date = models.DateField('Стартовал', blank=True, null=True)
    end_date = models.DateField('Завершился', blank=True, null=True)
    comment = RichTextUploadingField('Описание', blank=True, null=True)
    missing_info = RichTextUploadingField('Не хватает', blank=True, null=True)
    total_pay = models.DecimalField('Оплачено', decimal_places=2, max_digits=10, blank=False, null=True, default=0)

    is_done = models.BooleanField(default=False, blank=True)
    is_dead_line_soon = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



class OrderFile(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False, null=True, related_name='files')
    file = models.FileField(upload_to='order/file', blank=False, null=True)
    description = models.CharField(max_length=255, blank=False, null=True)