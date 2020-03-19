from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Contact

admin.site.register(Profile)
admin.site.register(Contact)



UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff',
        'followers','total_followers',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
