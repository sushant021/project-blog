from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

DEFAULT_CATEGORY =1 

class ActiveManager(models.Manager):
	def get_queryset(self):
		return super(ActiveManager,self).get_queryset().filter(active=True)


class Category(models.Model):
	name=models.CharField(max_length=100)
	slug=models.SlugField(max_length=100)

	class Meta:
		ordering=('name',)
		verbose_name='Category'
		verbose_name_plural='Categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('blog:category_archive',args=[self.slug])

class Post(models.Model):
	STATUS_CHOICES= (('draft','Draft'),('published','Published'),)
	title=models.CharField(max_length=200)
	slug=models.SlugField(max_length=200)
	author=models.ForeignKey(User,on_delete=models.PROTECT,default='sushant')
	category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='posts',default=DEFAULT_CATEGORY)
	featured_image= models.ImageField(upload_to='post_featured_images/')
	status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='draft')
	content=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	published=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name='Post'
		verbose_name_plural='Posts'
		ordering=('-created',)
		
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_content',args=[self.slug])

class Comment(models.Model):
	post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
	name=models.CharField(max_length=200)
	email=models.EmailField()
	body=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	active=models.BooleanField(default=True)
	objects = models.Manager() # the default manager
	ActiveComments = ActiveManager() # custom manager that retrieves active comments 

	class Meta:
		verbose_name='comment'
		verbose_name_plural='comments'

	def __str__(self):
		return 'comment on {}  by {}'.format(self.post,self.name)

