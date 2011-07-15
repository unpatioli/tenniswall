from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, CreateView
from accounts.forms import RegistrationForm, UserprofileForm
from accounts.models import UserProfile

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

class ProfileView(DetailView):
    model = UserProfile

    def get(self, request, **kwargs):
        if (request.user.is_authenticated()
            and int(self.kwargs.get('pk', None)) == request.user.id):
            return redirect('accounts_my_profile')
        return super(ProfileView, self).get(request, **kwargs)

class MyProfileView(DetailView):
    model = UserProfile

    def get_object(self, queryset=None):
        try:
            userprofile = self.request.user.get_profile()
        except UserProfile.DoesNotExist:
            userprofile = None
        return userprofile

    def render_to_response(self, context, **response_kwargs):
        if not self.object:
            return redirect('accounts_my_profile_new')
        return super(MyProfileView, self).render_to_response(context, **response_kwargs)

class MyProfileCreateView(CreateView):
    model = UserProfile
    form_class = UserprofileForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, _('User profile is created'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, _('User profile is not created'))
        return super(MyProfileCreateView, self).form_invalid(form)
        
