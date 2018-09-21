from django.contrib import admin
from msguide.models import UserProfile
# Register your models here.
admin.site.register(UserProfile)

admin.site.site_header = 'MS Guidance Admininstration'
