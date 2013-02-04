from datetime import date, datetime

from django.forms import widgets
from django import forms

class DateSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None, dt=None, mode=0):
        months = []
        for i in range(1,13):
            months.append((i, date(2000,i,1).strftime("%B")))
        days = [(day,day) for day in range(1,32)]
        years = [(year, year) for year in range(1900,2013)]

        _widgets = (
            widgets.Select(attrs=attrs, choices=days), 
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=years),
            )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        try:
            if value:
                return [value.day, value.month, value.year]
            return [None, None, None]
        except AttributeError:
            return value

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            D = date(day=int(datelist[0]), month=int(datelist[1]),
                    year=int(datelist[2]))
        except ValueError:
            return ''
        else:
            return str(D)
