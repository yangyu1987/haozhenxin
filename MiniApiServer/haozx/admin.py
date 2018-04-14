from django.contrib import admin

# Register your models here.
from .models import Haozx


class HaozxAdmin(admin.ModelAdmin):
    list_display = ['id', 'phoneNum', 'name', 'idCard', 'smsCode', 'smsSend', 'codeUsed','timestamp','result']
    search_fields = ['phoneNum', 'name', 'idCard', 'smsCode', 'smsSend', 'codeUsed','timestamp','result']
    # list_filter = ['phoneNum', 'name', 'idCard', 'smsCode', 'smsSend','token', 'codeUsed','timestamp','result']


admin.site.register(Haozx,HaozxAdmin)