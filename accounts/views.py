from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.functional import lazy
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, CreateView, UpdateView, TemplateView
from accounts.forms import  UserprofileForm, NewUserForm
from accounts.models import UserProfile

class RegistrationView(CreateView):
    model = User
    form_class = NewUserForm
    template_name = 'accounts/user_form.html'
    success_url = lazy(reverse, str)('accounts_register_thankyou')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        self.request.session['registered_user_name'] = username
        messages.success(self.request, _('User is registered'))
        return super(RegistrationView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('User is not registered'))
        return super(RegistrationView, self).form_invalid(form)

class ThankyouView(TemplateView):
    template_name = 'accounts/thankyou.html'

    def get_context_data(self, **kwargs):
        registered_user_name = self.request.session.get(
            'registered_user_name', False
        )

        try:
            del self.request.session['registered_user_name']
        except KeyError:
            pass

        context = super(ThankyouView, self).get_context_data(**kwargs)
        context['registered_user_name'] = registered_user_name
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context.get('registered_user_name', False):
            return self.render_to_response(context)
        return redirect('root')

class ProfileView(DetailView):
    model = UserProfile

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(UserProfile, user__pk=pk)

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

    def get(self, request, *args, **kwargs):
        if self._check_profile_exists(request.user):
            return redirect('accounts_my_profile')
        return super(MyProfileCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self._check_profile_exists(request.user):
            return redirect('accounts_my_profile')
        return super(MyProfileCreateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, _('User profile is created'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, _('User profile is not created'))
        return super(MyProfileCreateView, self).form_invalid(form)

    def _check_profile_exists(self, user):
        return UserProfile.objects.filter(user=user).exists()

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
