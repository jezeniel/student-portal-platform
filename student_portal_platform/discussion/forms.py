from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

from .models import Thread, Post, SubjectThread


class ThreadForm(forms.ModelForm):
    title   = forms.CharField(label='')
    content = forms.CharField(label='',
                              widget=forms.Textarea)

    class Meta:
        model = Thread
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Fieldset(
                "Create a Topic",
                Field("title", css_class="span12", placeholder = "Title"),
                Field("content", css_class="span12", placeholder = "Content"),
            ),
            ButtonHolder(
                Submit("submit", "Create Topic", css_class="btn btn-large pull-right",
                       data_loading_text="Posting..."
                )
            )
        )
        return super(ThreadForm, self).__init__(*args, **kwargs)

class SubjectThreadForm(forms.ModelForm):
    title   = forms.CharField(label='')
    content = forms.CharField(label='',
                              widget=forms.Textarea)

    class Meta:
        model = SubjectThread
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Fieldset(
                "Create a Topic",
                Field("title", css_class="span12", placeholder = "Title"),
                Field("content", css_class="span12", placeholder = "Content"),
            ),
            ButtonHolder(
                Submit("submit", "Create Topic", css_class="btn btn-large pull-right",
                       data_loading_text="Posting..."
                )
            )
        )
        return super(SubjectThreadForm, self).__init__(*args, **kwargs)


class ReplyForm(forms.ModelForm):
    content = forms.CharField(label='', max_length=100,
                              widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('title', 'content')


class QuickReplyForm(forms.ModelForm):
    content = forms.CharField(label='',
                              widget=forms.Textarea,
                              required=True)
    next = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Post
        fields = ('content', 'next')

    def __init__(self, *args, **kwargs):
        super(QuickReplyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_tag = False
        self.helper.form_class = "id-quickreply"
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Fieldset(
                "Quick Reply",
                Field("content", css_class="span12"),
                Field("next"),
            ),
            ButtonHolder(
                Submit("submit", "Quick Reply", css_class="btn btn-large pull-right", data_loading_text="Posting..."),
            )
        )

        return super(QuickReplyForm, self).__init__(*args, **kwargs)
