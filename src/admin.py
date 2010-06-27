from models import *
from django.contrib import admin

class RecordAdmin(admin.TabularInline):
	model = Record

class AddressInline(admin.TabularInline):
	model = Address

class ZoneAdmin(admin.ModelAdmin):
	inlines = [AddressInline,RecordAdmin]

class AddressAdmin(admin.ModelAdmin):
	list_display = ('ip', 'prefix_len', 'subnet', 'device')

class ContactAdmin(admin.ModelAdmin):
	list_display = ('nick', 'name', 'email')

class DeviceAdmin(admin.ModelAdmin):
	inlines = [AddressInline,]
	list_display = ('name', 'contact', 'type', 'os', 'info')
	list_filter = ('contact', 'type', 'os')

admin.site.register(Zone, ZoneAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(OperatingSystem)
admin.site.register(DeviceType)
admin.site.register(Contact, ContactAdmin)
