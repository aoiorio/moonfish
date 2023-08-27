from django.contrib import admin

# Food DB をこのアプリの中で使用できるようにしている（/adminに行った時に、Food DBが表示されるようにする）
from .models import Food
admin.site.register(Food)
