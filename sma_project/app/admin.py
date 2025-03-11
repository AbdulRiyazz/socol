from django.contrib import admin
from app.models import account_profile
from app.models import Post

# Register your models here.
admin.site.register(account_profile)
admin.site.register(Post)