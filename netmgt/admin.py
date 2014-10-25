from netmgt.models import *
from django.contrib import admin
from forms import *

class ZoneRecordAdmin(admin.TabularInline):
	model = ZoneRecord
	form  = ZoneRecordForm

class TemplateRecordAdmin(admin.TabularInline):
	model = TemplateRecord
	form  = TemplateRecordForm

class AddressInline(admin.TabularInline):
	model = Address
	exclude = ('reverse_zone',)

class ZoneAdmin(admin.ModelAdmin):
	form = ZoneAdminForm
	inlines = [AddressInline, ZoneRecordAdmin]

class TemplateAdmin(admin.ModelAdmin):
	inlines = [TemplateRecordAdmin]

class AddressAdmin(admin.ModelAdmin):
	list_display = ('ip', 'prefix_len', 'subnet', 'reverse_zone', 'device')

class ContactAdmin(admin.ModelAdmin):
	list_display = ('nick', 'name', 'email')

class DeviceAdmin(admin.ModelAdmin):
	inlines = [AddressInline,]
	list_display = ('name', 'contact', 'type', 'os', 'info')
	list_filter = ('contact', 'type', 'os')

admin.site.register(Template, TemplateAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Device, DeviceAdmin)
#admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(OperatingSystem)
admin.site.register(DeviceType)
#admin.site.register(CachedZone)
admin.site.register(Contact, ContactAdmin)
