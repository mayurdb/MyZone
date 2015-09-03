from django.contrib import admin
from .models import *

# Register your models here.

class ChildInline(admin.StackedInline):
    model = Child
    extra = 0

class User_Profile_Admin(admin.ModelAdmin):
    fieldsets = [
        ('Confirmation_key',               {'fields': ['confirmation_key']}),
        ]  
    inlines = [ChildInline]      

admin.site.register(User_profile, User_Profile_Admin)
admin.site.register(Child)
admin.site.register(Friendship)
admin.site.register(Friend_request)