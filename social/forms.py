from socialregistration.forms import UserForm

class Profile(UserForm):
    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        if 'email' in self.fields:
            del self.fields['email']

    def clean(self):
        self.cleaned_data['email'] = ''
        return super(Profile, self).clean()
