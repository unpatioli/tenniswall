# Create your views here.
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.views.generic import CreateView, TemplateView, UpdateView
from django.utils.translation import ugettext as _
from walls.forms import WallForm
from walls.models.models import Wall

class IndexView(TemplateView):
    template_name = 'walls/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'free_walls': Wall.free.all()[:10],
            'paid_walls': Wall.paid.all()[:10],
        })
        return context

class AddWallView(CreateView):
    model = Wall
    form_class = WallForm
    
#    def get_initial(self):
#        initials = super(AddWallView, self).get_initial()
#        initials.update({'reported_by': self.request.user})
#        return initials
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.reported_by = self.request.user
        self.object.save()
        messages.success(self.request, _('Wall saved'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, _('Wall is not saved'))
        return super(AddWallView, self).form_invalid(form)

class EditWallView(UpdateView):
    model = Wall
    form_class = WallForm

    def get_object(self, queryset=None):
        wall = super(EditWallView, self).get_object(queryset)
        if not wall.can_edit(self.request.user):
            raise Http404
        return wall

    def form_valid(self, form):
        messages.success(self.request, _('Wall is updated'))
        return super(EditWallView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Wall is not updated'))
        return super(EditWallView, self).form_invalid(form)
