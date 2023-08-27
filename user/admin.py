from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

class UserNetworkInline (admin.StackedInline):
    model = UserNetwork
    extra = 0

class UserCommentInline (admin.StackedInline):
    model = UserComment
    extra = 0

class UserAdmin(BaseUserAdmin):
    list_display = (
        'login',
        'fio',
        'phone',
        'date_joined',

    )
    ordering = ('id',)
    inlines = [UserNetworkInline,UserCommentInline]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "avatar",
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
             'avatar',
             'added_by',
             'email',
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
admin.site.register(UserNetworks)
admin.site.register(UserComment)



