from django.contrib import admin
from account.models import UserProfile, Company , User
admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(User)

# Register your models here.
