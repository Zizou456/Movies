from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import USER


# Register your models here.

class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined')
	search_fields = ('email','username',)
	readonly_fields=('id', 'date_joined')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(USER, AccountAdmin)
