from django import forms

class CalendarWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        from django.utils.safestring import mark_safe
        res = super(CalendarWidget, self).render(name, value, attrs=attrs)
        if attrs and 'id' in attrs:
            res += mark_safe(u"""
                <script type="text/javascript">
                    $(function() {
                        $( "#%s" ).datepicker({
                            changeYear: true,
                            changeMonth: true,
                            yearRange: '-90:+00',
                            defaultDate: '-18y',
                        });
                    });
                </script>
            """ % attrs['id'])
        return res
