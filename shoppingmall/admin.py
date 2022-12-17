from django.contrib import admin
from .models import Toy, Maker, Category, Material, Comment
# Register your models here.

admin.site.register(Toy)
# name필드 값으로 slug 자동 생성
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}   # 카테고리가 자동으로 slug로 만들어짐?
admin.site.register(Category, CategoryAdmin)
class MaterialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}   # 카테고리가 자동으로 slug로 만들어짐?
admin.site.register(Material, MaterialAdmin)
admin.site.register(Maker)
admin.site.register(Comment)