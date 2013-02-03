from django.forms import widgets

class DateSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None, dt=None, mode=0):  
        months = [(month,month) for month in ["Jan", "Feb", "March"]]
        days = [(day,day) for day in range(1,32)]
        years = [(year, year) for year in range(1900,2013)]

        _widgets = (
            widgets.Select(attrs=attrs, choices=days), 
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=years),
            )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.day, value.month, value.year]
        return [None, None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)
