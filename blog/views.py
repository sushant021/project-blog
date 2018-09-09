from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Category
from .forms import SharePostForm,CommentForm
from django.core.mail import send_mail
from django.contrib import messages


def index(request):
	posts=Post.objects.filter(status='published')
	return render(request,'blog/index.html',{'posts':posts})

def post_content(request,post_slug):
    post= Post.objects.get(slug=post_slug)
    
    new_comment=None
    
    #get all comments that are currently active to show in the post, this queryset is not evaluated yet, it will be 
    # evaluated in the template during iteration. 
    comments= post.comments.filter(active=True)

    

    #see if there are any comments already 
    comment_exists = post.comments.filter(active=True).exists()

    if request.method=='POST':
    	comment_form= CommentForm(request.POST)
    	if comment_form.is_valid():
    		# saving a ModelForm creates an object of the corresponding model. In this case, we need to create a comment
    		# object but we haven't assigned it a post yet, so we just temporarily save it in memory(not in database)
    		# commit=False does exactly this job. And later we save it in the database after assigning post. 
    		new_comment= comment_form.save(commit=False)
    		new_comment.post=post
    		new_comment.save()
    		messages.info(request,'Comment Posted Successfully',extra_tags='comment_posted')
    		# incase of successful submission you should always use redirect rather than render because of the 
    		# "resubmission if refreshed" problem  and it may have other benefits too, yet to explore ! 
    		return redirect(post)
    	else:
    		messages.error(request,'Comment details are invalid. Probably email!', extra_tags='invalid_comment')
    		
    else:
    	comment_form=CommentForm()
    return render(request,'blog/post_content.html',{'post':post,'comments':comments,'comment_form':comment_form,'comment_exists':comment_exists})
	

def category_archive(request,category_slug):
	category=Category.objects.get(slug=category_slug)
	posts= category.posts.all()
	return render(request,'blog/category_archive.html',{'category':category,'posts':posts})

def share_post(request,post_slug):
	post=get_object_or_404(Post,slug=post_slug)
	
	sent=False
	if request.method=='POST':
		form=SharePostForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			post_url= request.build_absolute_uri(post.get_absolute_url())
			subject='{} recommends you reading {}'.format(cd['name'],post.title)
			message= "{}({}) suggests you to read this: {} \n at {} \n His comments: \n {} ".format(cd['name'],cd['email'], post.title,post_url,cd['comment'])
			receiver=cd['to']
			send_mail(subject,message,'code.breakit@gmail.com',[receiver])
			sent=True
			share_success_message= " Post sucessfully shared with {}".format(receiver)
			messages.info(request,share_success_message,extra_tags='post_shared')
			return redirect(post)

	else:
		form=SharePostForm()
	return render(request,'blog/share_post.html',{'post':post,'form':form,'sent':sent})