from django import forms

from crispy_forms.layout import Layout, Field, ButtonHolder, Fieldset, Submit
from crispy_forms.helper import FormHelper


class LectureForm(forms.Form):
	chapter = forms.CharField(max_length = 100)
	content = forms.CharField(widget = forms.Textarea)

	def __init__(self, *args, **kwargs):
		super(LectureForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.html5_required = True

		self.helper.layout = Layout (
				Fieldset(
						"Create Lecture",
						Field('chapter'),
						Field('content'),
					),
				ButtonHolder(
						Submit('submit', 'Create Lecture'),
					)
			)

class LectureUploadForm(forms.Form):
	docfile = forms.FileField(label = "Select a file", help_text="max. 42 megabytes")

	def __init__(self, *args, **kwargs):
		super(LectureUploadForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tags = False
		self.helper.html5_required = True
		self.helper.layout = Layout(
				Field("docfile"),
			)

