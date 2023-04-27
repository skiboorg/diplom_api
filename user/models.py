import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone
from datetime import timedelta
# from .tasks import send_email

import logging
logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, login, password, **extra_fields):
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login, password, **extra_fields)

    def create_superuser(self, login, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(login, password, **extra_fields)




class User(AbstractUser):
    username = None
    firstname = None
    lastname = None
    added_by = models.ForeignKey('self',on_delete=models.CASCADE, blank=True, null=True, related_name='user_added_by')
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    login = models.CharField('Логин', max_length=20, blank=True, null=True, unique=True)
    email = models.CharField('Почта', max_length=20, blank=True, null=True)
    fio = models.CharField('ФИО', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)



    is_private = models.BooleanField('Частный\контрагент', default=False)
    is_vip = models.BooleanField('важный', default=False)
    is_problem = models.BooleanField('проблемный', default=False)
    is_manager = models.BooleanField('Менедждер', default=False)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.fio} {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = '1. Пользователи'

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True, related_name='files')
    file = models.FileField(upload_to='user/file', blank=False, null=True)
    description = models.CharField(max_length=255, blank=False, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)


class UserNetworks(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    icon = models.TextField(blank=False, null=True)

    def __str__(self):
        return f'{self.name}'

class UserNetwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True, related_name='networks')
    network = models.ForeignKey(UserNetworks, on_delete=models.CASCADE, blank=False, null=True)
    link = models.CharField(max_length=255, blank=False, null=True)

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True, related_name='comments')
    text = models.TextField(blank=False, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)

def user_post_save(sender, instance, created, **kwargs):
    #import monthdelta
    #datetime.date.today() + monthdelta.monthdelta(months=1)

    if created:
        print('created')


post_save.connect(user_post_save, sender=User)


