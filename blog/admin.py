from django.contrib import admin
from .models import Category,Post,Comment

@admin.register(Category)
class modelCategory(admin.ModelAdmin):
	list_display=['name','slug']
	prepopulated_fields={'slug':('name',)}

@admin.register(Post)
class modelsPost(admin.ModelAdmin):
	list_display=['title','slug','author','category','created','updated']
	list_filter=['category','updated','created']
	prepopulated_fields={'slug':('title',)}

@admin.register(Comment)
class modelComment(admin.ModelAdmin):
	list_display=['name','email','post','created','active','body']
	list_filter=['created','updated']
	list_editable=['active']
	search_fields= ['name','email','body']
