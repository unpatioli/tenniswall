from django.core.urlresolvers import reverse
from django.db import models
from sorl.thumbnail import ImageField, delete
from walls import Wall
from util import Timestamps

class WallImage(Timestamps):
    wall = models.ForeignKey(Wall)

    image = ImageField(upload_to='wall_images')
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'walls'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('walls_images_detail', args=[self.wall_id, self.pk,])

    def delete(self, using=None):
        delete(self.image)
        super(WallImage, self).delete(using)
