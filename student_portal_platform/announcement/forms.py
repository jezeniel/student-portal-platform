from django import forms

class AnnouncementForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget= forms.Textarea);
    
