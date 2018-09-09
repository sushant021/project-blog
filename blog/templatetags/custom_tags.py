from django import template
from  blog.models import Category,Post,Comment

register= template.Library()

@register.simple_tag
def get_categories():
	categories= Category.objects.exclude(slug = 'uncategorized')
	return categories

@register.simple_tag
def get_all_categories():
	categories=Category.objects.all()
	return categories

#@register.filter
#def get_category_len(category_slug):
#	category= Category.objects.get(slug=category_slug)
#	posts= category.posts.all()
#	return len(posts)


@register.simple_tag
def recent_posts():
	recent_posts= Post.objects.all()[:8]
	return recent_posts

@register.filter
def allcaps(post_title):
	post_title_caps=post_title.upper()
	return post_title_caps
	
@register.simple_tag
def recent_comments():
	recent_comments= Comment.ActiveComments.all()[:5]
	return recent_comments

@register.filter
def cap_initials(anystring):
	cap_text=""
	for word in anystring.split():
		cap_text= cap_text+word.capitalize()+" "

	return cap_text


