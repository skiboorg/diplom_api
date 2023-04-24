from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

class UserAdmin(BaseUserAdmin):
    list_display = (
        'login',
        'fio',
        'phone',
        'date_joined',

    )
    ordering = ('id',)
    #inlines = []
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "login",
                "fio",
                "phone",
                "is_private",
                "is_vip",
                "is_problem",
                "is_manager",
                       'password1',
                       'password2',
                       ), }),)
    search_fields = ('id','login', 'fio', 'phone',)
    list_filter = (
        "is_private",
                "is_vip",
                "is_problem",
                "is_manager",
                   )
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Personal info',
         {'fields': (
             'added_by',
             'email',
             'comment',
                "fio",
                "phone",
                "is_private",
                "is_vip",
                "is_problem",
                "is_manager",

         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',)}),)

admin.site.register(User,UserAdmin)



