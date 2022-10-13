from django.contrib import admin
from .models import *
# Register your models here.

class admin_list(admin.ModelAdmin):
    list_display= ("name", "cur_bid","date", "created_by")

admin.site.register(info_bid)
admin.site.register(auction_item,admin_list)
admin.site.register(cmt)
admin.site.register(categories)