from django import forms

from .models import Thread, Post

class ThreadForm(forms.ModelForm):
    content = forms.CharField(label='', max_length=100,
                              widget = forms.Textarea)
    class Meta:
        model = Thread
        fields = ('title', 'content')

class ReplyForm(forms.ModelForm):
    content = forms.CharField(label='', max_length=100,
                              widget = forms.Textarea)
    class Meta:
        model = Post
        fields = ('title', 'content')
        
class QuickReplyForm(forms.ModelForm):
    content = forms.CharField(label='', max_length=100,
                              widget = forms.Textarea)
    
    class Meta:
        model = Post
        fields = ('content',)
    