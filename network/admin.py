from django.contrib import admin
from .models import User, Thread

# Register your models here.

admin.site.register(User)
admin.site.register(Thread)