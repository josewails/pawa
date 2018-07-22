from django.contrib import admin

from .models import User, FacebookUser

class FaceBookUserAdmin(admin.ModelAdmin):

    class Meta:
        list_display = ['facebook_id', 'name']
        model = FacebookUser

admin.site.register(User)
admin.site.register(FacebookUser, FaceBookUserAdmin)