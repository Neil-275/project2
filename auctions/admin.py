from django.contrib import admin
from .models import info_bid,auction_item,cmt
# Register your models here.

class admin_list(admin.ModelAdmin):
    list_display= ("name", "cur_bid","date", "created_by")

admin.site.register(info_bid)
admin.site.register(auction_item,admin_list)
admin.site.register(cmt)