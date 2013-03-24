from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class PersonalMessageForm(forms.Form):
    title = forms.CharField(max_length=255, label=(""))
    content = forms.CharField(widget=forms.Textarea, label=(""))

    def __init__(self, *args, **kwargs):
        super(PersonalMessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.html5_required = True

        self.helper.layout = Layout(
            Field("title", css_class="span12", placeholder="Title"),
            Field("content", css_class="span12", placeholder="Type your message here..."),
        )
