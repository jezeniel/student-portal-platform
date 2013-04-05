from datetime import datetime

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Fieldset, Layout, Submit, ButtonHolder
from crispy_forms.bootstrap import AppendedText

class AddSubjectForm(forms.Form):
    name = forms.CharField(label=u"Subject Name", max_length=100)
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        super(AddSubjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.layout = Layout(
                    Field("name", css_class="span10"),
                    AppendedText("start_date",
                             "<i class='icon-calendar' data-time-icon='icon-time' data-date-icon='icon-calendar'></i>",
                             css_class="datepicker", template="official/crispy/appended_datepicker.html",
                             readonly=True),
                    AppendedText("end_date",
                             "<i class='icon-calendar' data-time-icon='icon-time' data-date-icon='icon-calendar'></i>",
                             css_class="datepicker", template="official/crispy/appended_datepicker.html",
                             readonly=True),
            )

    def clean(self):
        cleaned_data = super(AddSubjectForm,self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if end_date and start_date:
            if end_date < start_date:
                self._errors['start_date'] = self.error_class(["Invalid start date!"])
                del cleaned_data['start_date']
                del cleaned_data['end_date']
        return cleaned_data

