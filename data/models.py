from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import uuid
from pytils.translit import slugify

class Banner(models.Model):
    image = models.FileField('Картинка', upload_to='banner/', blank=False, null=True)
    url = models.CharField('Ссылка', max_length=255, blank=True, null=True)
    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннер'

class Category(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    price_from = models.IntegerField('Цена от', blank=False, null=True)
    image = models.FileField('Картинка', upload_to='category/', blank=False, null=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.name_slug:
            self.name_slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

class Direction(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.name_slug:
            self.name_slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направление'

class Country(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    flag = models.FileField('Флаг', upload_to='flags/', blank=False, null=True)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, blank=False, null=True, related_name='countries')
    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.name_slug:
            self.name_slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страна'

class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=True, related_name='services')
    countries = models.ManyToManyField(Country, blank=False)
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    info_text = models.TextField('Текст описания', blank=True, null=True)
    warn_text = models.TextField('Текст предупреждения', blank=True, null=True)
    info_tab = RichTextUploadingField('Содержимое информационного таба', blank=True, null=True)
    price = models.IntegerField('Цена', blank=False, null=True)
    work_time = models.CharField('Срок исполнения', max_length=255, blank=True, null=True)
    icon = models.FileField('Иконка', upload_to='service/', blank=False, null=True)
    image = models.FileField('Картинка', upload_to='category/', blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.name_slug:
            self.name_slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуга'

class ServiceTab(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=False, null=True, related_name='tabs')
    body = RichTextUploadingField('Содержимое таба', blank=True, null=True)
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Таб'
        verbose_name_plural = 'Таб'

class PayStatus(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    color = models.CharField('Цвет (red - красный, green - зеленый, blue - синий, yellow - желтый)',
                             max_length=255, blank=False, null=True)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Статус оплаты'
        verbose_name_plural = 'Статус оплаты'

class OrderStatus(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    color = models.CharField('Цвет (red - красный, green - зеленый, blue - синий, yellow - желтый)',
                             max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статус заказа'

class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=False, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=False, null=True)
    pay_status = models.ForeignKey(PayStatus, on_delete=models.SET_NULL, blank=True, default=1, null=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, blank=True, default=1, null=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True,related_name='created_by')
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
    created_at = models.DateField(auto_now_add=True, null=True)

class OrderComment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False, null=True, related_name='comments')
    text = models.TextField(blank=False, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)