from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Book_info)
admin.site.register(Stock_bill)
admin.site.register(Guest_bill)
admin.site.register(Bill)
admin.site.register(Finance)