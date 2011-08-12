# Create your views here.
from django.contrib import messages
from django.contrib.gis.geos import Polygon
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.utils.translation import ugettext as _
from django.views.generic.detail import   DetailView
from walls.forms import WallForm, WallCommentForm, WallImageForm
from walls.models import Wall, WallComment, WallImage

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
        messages.success(self.request, _('Your comment is posted'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, _('Your comment was not posted'))
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
        qs = Wall.objects.all()
        if self.request.user.is_authenticated():
            qs |= Wall.all_walls.filter(reported_by=self.request.user)
        return qs


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

            wall_type = json_data.get('wall_type')
            if (wall_type and
                not (isinstance(wall_type, (list, tuple))
                     or getattr(wall_type, '__iter__', False))):
                wall_type = [wall_type]

            qs = Wall.objects.none()

            if 'free' in wall_type:
                qs |= Wall.free.all()
            if 'paid' in wall_type:
                qs |= Wall.paid.all()

            # Get walls in bbox
            walls = qs.filter(location__contained=bbox_polygon)[:num]

            # Assemble walls list
            markers = [{
                'lat': wall.location.x,
                'lng': wall.location.y,
                'title': unicode(wall),
                'is_paid': wall.is_paid(),
                'info': wall.description,
                'url': wall.get_absolute_url(),
                'link_title': _('Details')
            } for wall in walls]

            return HttpResponse(simplejson.dumps(markers),
                                mimetype="application/json; charset=utf-8")
    raise Http404


class WallImagesMixin(object):
    """
    Provides common methods for nested WallImage objects
    """
    model = WallImage
    form_class = WallImageForm

    # regulates adding current user's walls to queryset if they are not approved
    allow_self_walls = False
    # current wall cache
    wall = None

    def get_queryset(self):
        """
        Adds current wall to cache (self.wall) before return queryset
        :return: Current wall's images queryset
        """
        self._get_wall()
        return self.wall.wallimage_set.all()

    def _get_wall(self, force=False):
        """
        Gets Wall object by wall_pk parameter
        :param force: Not to check if self.wall already exists
        :raise: Http404 if wall_pk corresponds to missing wall
        """
        if not self.wall or force:
            wall_pk = self.kwargs['wall_pk']
            qs = Wall.objects.all()
            if self.allow_self_walls:
                qs |= Wall.all_walls.filter(reported_by=self.request.user)
            try:
                self.wall = qs.get(pk=wall_pk)
            except Wall.DoesNotExist:
                raise Http404

    def _assert_can_edit_wall(self, wall=None):
        """
        Checks if current user can edit wall
        :param wall: Wall to check against instead of cached wall
        :raise: Http404 if user can't edit wall
        """
        if not wall:
            self._get_wall()
            wall = self.wall
        if not wall.can_edit(self.request.user):
            raise Http404


class WallImagesListView(WallImagesMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super(WallImagesListView, self).get_context_data(**kwargs)
        context.update({
            'wall_pk': self.kwargs['wall_pk'],
            })
        return context


class WallImagesListEditView(WallImagesListView):
    template_name = 'walls/wallimage_list_edit.html'
    allow_self_walls = True

    def get_queryset(self):
        self._assert_can_edit_wall()
        return super(WallImagesListEditView, self).get_queryset()


class WallImagesDetailView(WallImagesMixin, DetailView):
    allow_self_walls = True


class WallImagesEditView(WallImagesMixin, UpdateView):
    allow_self_walls = True

    def get_object(self, queryset=None):
        wall_image = super(WallImagesEditView, self).get_object(queryset)
        self._assert_can_edit_wall(wall_image.wall)
        return wall_image

    def get_success_url(self):
        return reverse('walls_images_list_edit', args=[self.object.wall_id, ])

    def get_context_data(self, **kwargs):
        context = super(WallImagesEditView, self).get_context_data(**kwargs)
        context.update({
            'wall_pk': self.kwargs['wall_pk'],
            })
        return context


class WallImagesDeleteView(WallImagesMixin, DeleteView):
    allow_self_walls = True

    def get_object(self, queryset=None):
        wall_image = super(WallImagesDeleteView, self).get_object(queryset)
        self._assert_can_edit_wall(wall_image.wall)
        return wall_image

    def get_success_url(self):
        return reverse('walls_images_list', args=[self.object.wall_id, ])


class WallImagesAddView(WallImagesMixin, CreateView):
    allow_self_walls = True

    def render_to_response(self, context, **response_kwargs):
        self._assert_can_edit_wall()
        return super(WallImagesAddView, self).render_to_response(
            context, **response_kwargs
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.wall_id = self.kwargs['wall_pk']
        self.object.save()
        messages.success(self.request, _('Wall image saved'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, _('Wall image is not saved'))
        return super(WallImagesAddView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('walls_images_list_edit', args=[self.object.wall_id, ])

    def get_context_data(self, **kwargs):
        context = super(WallImagesAddView, self).get_context_data(**kwargs)
        context.update({
            'wall_pk': self.kwargs['wall_pk'],
            })
        return context
