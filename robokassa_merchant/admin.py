# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from robokassa_merchant.models import *


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object_link', 'create_date', 'payment_date',
                    'total_price', 'current_status', 'user')
    list_filter = ('current_status',)
    date_hierarchy = 'create_date'
    list_display_links = ('id', )
    # убираем возможность редактировать из админки всё, кроме описания
    readonly_fields = ('content_type', 'object_id', 'content_object', 'create_date',
                       'payment_date', 'total_price', 'current_status', 'user', )

    # поле Связанного объекта
    def content_object_link(self, obj):
        res = None
        if obj.content_object:
            content_object_admin_url_pattern = 'admin:{}_{}_change'.format(
                obj.content_object._meta.app_label.lower(),
                obj.content_object._meta.model_name.lower(),
            )
            content_object_admin_url = reverse(content_object_admin_url_pattern, args=(obj.content_object.id,))
            res = mark_safe('{}: <a href="{}">{}</a>'.format(
                obj.content_type,
                content_object_admin_url,
                obj.content_object
            ))
        return res
    content_object_link.allow_tags = True
    content_object_link.short_description = 'Связанный объект'

    # убираем возможность что-либо делать в админке, кроме просмотра списка
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


class EventAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'create_date', 'status', 'message')
    list_filter = ('status',)
    date_hierarchy = 'create_date'
    readonly_fields = Event._meta.get_all_field_names()
    list_display_links = None

    # убираем возможность что-либо делать в админке, кроме просмотра списка
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Event, EventAdmin)
