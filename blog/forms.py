from django import forms
from .models import Comment

class SharePostForm(forms.Form):
	name=forms.CharField()
	email=forms.EmailField()
	to=forms.EmailField()
	comment= forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields= ('name','email','body')
		widgets={
		 'body':forms.Textarea(attrs={'rows':'3','cols':'60'})
		}