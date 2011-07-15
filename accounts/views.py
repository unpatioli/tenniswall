from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from accounts.forms import RegistrationForm

def register(request):
    from django.contrib.auth.models import User

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            messages.success(request, _('User is registered'))
            return redirect('/')
        else:
            messages.error(request, _('User is not registered'))
    else:
        form = RegistrationForm()

    return render(request, 'accounts/user_form.html', {'form': form})
