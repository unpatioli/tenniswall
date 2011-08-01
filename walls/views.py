# Create your views here.
from django.contrib import messages
from django.contrib.gis.geos import Polygon
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, ListView
from django.utils.translation import ugettext as _
from django.views.generic.detail import   DetailView
from walls.forms import WallForm, WallCommentForm
from walls.models import Wall, WallComment

class IndexView(TemplateView):
    template_name = 'walls/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'free_walls': Wall.free.all()[:10],
            'paid_walls': Wall.paid.all()[:10],
            })
        return context


class FreeListView(ListView):
    def get_queryset(self):
        return Wall.free.all() |\
               Wall.all_free.filter(reported_by=self.request.user)

class PaidListView(ListView):
    def get_queryset(self):
        return Wall.paid.all() |\
               Wall.all_paid.filter(reported_by=self.request.user)

class AddWallView(CreateView):
    model = Wall
    form_class = WallForm

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
    form_class = WallForm

    def get_queryset(self):
        return Wall.objects.all() |\
               Wall.all_walls.filter(reported_by=self.request.user)

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


class DeleteWallView(DeleteView):
    def get_queryset(self):
        return Wall.objects.all() |\
               Wall.all_walls.filter(reported_by=self.request.user)

    def get_object(self, queryset=None):
        wall = super(DeleteWallView, self).get_object(queryset)
        if not wall.can_delete(self.request.user):
            raise Http404
        return wall

    def get_success_url(self):
        return reverse('walls_index')

    def delete(self, request, *args, **kwargs):
        res = super(DeleteWallView, self).delete(request, *args, **kwargs)
        messages.success(request, _('Wall deleted'))
        return res


class CommentedDetailView(DetailView):
    comment_form_class = None
    comment_model = None
    comment_queryset = None
    comment_target_field_name = 'target'
    success_url = None

    def get_comment_form_class(self):
        return self.comment_form_class

    def get_comment_form(self, form_class):
        if self.request.method in ('POST', 'PUT',):
            return form_class(self.request.POST)
        return form_class()

    def get_comment_queryset(self):
        if self.comment_queryset is None:
            if self.comment_model:
                return self.comment_model._default_manager.all()
            else:
                raise ImproperlyConfigured()
        return self.comment_queryset._clone()

    def get_context_data(self, **kwargs):
        context = super(CommentedDetailView, self).get_context_data(**kwargs)
        context.update({
            'comments': self.get_comment_queryset().filter(**{
                self.comment_target_field_name: self.object,
                }),
            })
        return context

    def get_success_url(self):
        if not self.success_url:
            raise ImproperlyConfigured()
        return self.success_url

    def form_save(self, form):
        raise NotImplementedError

    def form_valid(self, form):
        self.form_save(form)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self._render_with_form(form)

    def get(self, request, **kwargs):
        form_class = self.get_comment_form_class()
        return self._render_with_form(self.get_comment_form(form_class))

    def post(self, request, *args, **kwargs):
        form_class = self.get_comment_form_class()
        comment_form = self.get_comment_form(form_class)
        if comment_form.is_valid():
            return self.form_valid(comment_form)
        else:
            return self.form_invalid(comment_form)

    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def _render_with_form(self, form):
        self.object = self.get_object()
        return self.render_to_response(
            self.get_context_data(
                object=self.object,
                comment_form=form
            )
        )


class CommentedWallDetailView(CommentedDetailView):
    comment_model = WallComment
    comment_form_class = WallCommentForm
    comment_target_field_name = 'wall'

    def get_queryset(self):
        return Wall.objects.all() |\
               Wall.all_walls.filter(reported_by=self.request.user)

    def get_success_url(self):
        return reverse('walls_detail', args=[self.object.pk, ])

    def form_save(self, form):
        self.object = self.get_object()
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.wall = self.object
        comment.ip = self.request.META.get("REMOTE_ADDR", None)
        comment.save()


def bbox(request):
    from django.utils import simplejson

    if request.is_ajax():
        if request.method == 'POST':
            # Process JSON with bbox
            json_data = simplejson.loads(request.raw_post_data)
            try:
                sw_lat = float(json_data['sw']['lat'])
                sw_lng = float(json_data['sw']['lng'])

                ne_lat = float(json_data['ne']['lat'])
                ne_lng = float(json_data['ne']['lng'])
            except (ValueError, KeyError):
                raise Http404

            # Create bbox
            bbox_coords = [
                (sw_lat, sw_lng),
                (sw_lat, ne_lng),
                (ne_lat, ne_lng),
                (ne_lat, sw_lng),
                (sw_lat, sw_lng),
            ]
            bbox_polygon = Polygon(bbox_coords)

            # Process walls limit number
            try:
                num = int(json_data.get('num', 2))
            except ValueError:
                num = 2

            wall_type = json_data.get('type', 'free')
            if wall_type == 'free':
                qs = Wall.free
            elif wall_type == 'paid':
                qs = Wall.paid
            else:
                qs = Wall.objects

            # Get walls in bbox
            walls = qs.filter(location__contained = bbox_polygon)[:num]

            # Assemble walls list
            markers = [{
                'lat': wall.location.x,
                'lng': wall.location.y,
                'title': unicode(wall),
                'info': wall.description,
                'url': wall.get_absolute_url(),
                'link_title': _('Details')
            } for wall in walls]

            return HttpResponse(simplejson.dumps(markers),
                                mimetype="application/json; charset=utf-8")
    raise Http404
