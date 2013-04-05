from random import shuffle

from django import forms

from crispy_forms.layout import Layout, Field, ButtonHolder, Fieldset, Submit
from crispy_forms.helper import FormHelper

class QuizForm(forms.Form):
    def __init__(self, data = None, questions = None, *args, **kwargs):
        super(QuizForm, self).__init__(data, *args, **kwargs)
        self.questions = questions
        for question in questions:
            field_name = "question_%d" % question.pk
            choices = [(choice.pk, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[field_name] = forms.ChoiceField(label = question.question, required = True,
                                                        choices = choices, widget = forms.RadioSelect)

class QuizUploadForm(forms.Form):
    xmlfile = forms.FileField(label = "Select a quiz file.", help_text="max. 42 megabytes")

    def __init__(self, *args, **kwargs):
        super(QuizUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tags = False
        self.helper.html5_required = True
        self.helper.layout = Layout(
                Field("xmlfile"),
            )
