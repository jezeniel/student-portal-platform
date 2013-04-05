from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

class AnnouncementForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget= forms.Textarea)


class SubjectAnnouncementForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self,*args, **kwargs):
        super(SubjectAnnouncementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
                    Field('title', css_class="span12"),
                    Field('content', css_class="span12"),
            )

