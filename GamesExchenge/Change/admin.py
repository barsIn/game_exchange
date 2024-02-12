from django.contrib import admin
from .models import Platform, Tags, Game, Goods


admin.site.register(Platform)
admin.site.register(Tags)
admin.site.register(Game)
admin.site.register(Goods)

# Register your models here.
