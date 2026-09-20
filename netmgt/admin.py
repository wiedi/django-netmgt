from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db import models as db_models
from django_object_actions import DjangoObjectActions, action

from netmgt.models import *

from .forms import *


class RecordInline(admin.TabularInline):
	formfield_overrides = {db_models.TextField: {"widget": AdminTextInputWidget}}


class ZoneRecordAdmin(RecordInline):
	model = ZoneRecord
	form = ZoneRecordForm


class TemplateRecordAdmin(RecordInline):
	model = TemplateRecord
	form = TemplateRecordForm


class AddressInline(admin.TabularInline):
	model = Address
	exclude = ("reverse_zone",)


class ZoneAdmin(DjangoObjectActions, admin.ModelAdmin):
	@action(label="Reset ACME Admin Token")
	def reset_acme_admin_token(self, request, obj):
		obj.acme_admin_token = ""
		obj.save()

	form = ZoneAdminForm
	inlines = [AddressInline, ZoneRecordAdmin]
	search_fields = ["name"]
	ordering = ["name"]
	readonly_fields = ["acme_admin_token"]
	change_actions = ["reset_acme_admin_token"]


class TemplateAdmin(admin.ModelAdmin):
	inlines = [TemplateRecordAdmin]
	search_fields = ["name"]
	ordering = ["name"]


class AddressAdmin(admin.ModelAdmin):
	list_display = ("ip", "prefix_len", "subnet", "reverse_zone", "device")
	search_fields = ["ip", "device"]
	ordering = ["ip"]


class ContactAdmin(admin.ModelAdmin):
	list_display = ("nick", "name", "email")
	search_fields = ["nick", "name", "email"]
	ordering = ["nick"]


class DeviceAdmin(admin.ModelAdmin):
	inlines = [
		AddressInline,
	]
	list_display = ("name", "contact", "type", "os", "info")
	list_filter = ("contact", "type", "os")
	search_fields = ["name"]
	ordering = ["name"]


admin.site.register(Template, TemplateAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Device, DeviceAdmin)
# admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(OperatingSystem)
admin.site.register(DeviceType)
# admin.site.register(CachedZone)
admin.site.register(Contact, ContactAdmin)
