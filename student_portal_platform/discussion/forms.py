from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder,Submit

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
                              widget = forms.Textarea,
                              required = True)
    
    class Meta:
        model = Post
        fields = ('content',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_tag = False
        self.helper.form_class = "id-quickreply"
        self.helper.html5_required = True
        self.helper.layout = Layout(
                                 Fieldset(
                                    "Quick Reply",
                                    "content"         
                                ),
                                ButtonHolder(
                                    Submit("submit","Quick Reply", css_class="btn btn-large pull-right"),
                                )
                            )
    
        return super(QuickReplyForm, self).__init__(*args,**kwargs)