# Create your views here.
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import CreateView
from django.utils.translation import ugettext as _
from walls.forms import FreeWallForm
from walls.models import FreeWall

def index(request):
    return render(request, 'walls/index.html')

class AddView(CreateView):
    model = FreeWall
    form_class = FreeWallForm
    
    def get_initial(self):
        initials = super(AddView, self).get_initial()
        initials.update({'reported_by': self.request.user})
        return initials
        
    def form_valid(self, form):
        messages.success(self.request, _('Wall saved'))
        return super(AddView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Wall is not saved'))
        return super(AddView, self).form_invalid(form)
