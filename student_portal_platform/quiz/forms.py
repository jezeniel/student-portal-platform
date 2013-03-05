from random import shuffle

from django import forms

class QuizForm(forms.Form):
    def __init__(self, data = None, questions = None, *args, **kwargs):
        super(QuizForm, self).__init__(data, *args, **kwargs)
        self.questions = questions
        for question in questions:
            field_name = "question_%d" % question.pk
            choices = [(choice.pk, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[field_name] = forms.ChoiceField(label = question.question, required = True,
                                                        choices = choices, widget = forms.RadioSelect)