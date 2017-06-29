from django.contrib import admin
from .models import Member,Bill, Transaction,WSGroup

admin.site.register(Bill)
admin.site.register(Member)
admin.site.register(WSGroup)
admin.site.register(Transaction)
