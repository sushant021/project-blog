from django.urls import path
from .import views

app_name='blog'

urlpatterns=[
path('',views.index,name='index'),
path('posts/<slug:post_slug>/',views.post_content,name='post_content'),
path('categories/<slug:category_slug>/',views.category_archive,name='category_archive'),
path('<slug:post_slug>/share-this-post/',views.share_post,name='share_post')
]