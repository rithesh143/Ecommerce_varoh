from django.contrib import admin
from .models import ContactUs,Address


# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
admin.site.register(ContactUs, ContactUsAdmin)

class AddressAdmin(admin.ModelAdmin):
    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'


    list_display = ('full_name', 'get_email', 'phone','pin_code','house','area','landmark','town','state')

admin.site.register(Address, AddressAdmin)