from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, CreateView, UpdateView
from accounts.forms import  UserprofileForm
from accounts.models import UserProfile

class RegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'

    def form_valid(self, form):
        messages.success(self.request, _('User is registered'))
        return super(RegistrationView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('User is not registered'))
        return super(RegistrationView, self).form_invalid(form)

class ProfileView(DetailView):
    model = UserProfile

    def get(self, request, **kwargs):
        if (request.user.is_authenticated()
            and int(self.kwargs.get('pk')) == request.user.id):
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

class MyProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserprofileForm

    def get_object(self, queryset=None):
        try:
            userprofile = self.request.user.get_profile()
        except UserProfile.DoesNotExist:
            userprofile = None
        return userprofile

    def form_valid(self, form):
        messages.success(self.request, _('User profile is updated'))
        return super(MyProfileEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('User profile is not updated'))
        return super(MyProfileEditView, self).form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        if not self.object:
            return redirect('accounts_my_profile_new')
        return super(MyProfileEditView, self).render_to_response(context, **response_kwargs)
