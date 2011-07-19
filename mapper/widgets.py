from django.contrib.gis.geos import GEOSGeometry, Point
from django.forms.util import flatatt
from django.forms.widgets import Widget
from django.utils.safestring import mark_safe

class GoogleMapPickLocationWidget(Widget):
    class Media:
        js = (
#            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.13/jquery-ui.min.js',

            'js/mapper/gmap.js',
        )
        css = {
            'all': (
                'css/mapper/gmap.css',
#                'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/sunny/jquery-ui.css',
            )
        }

    def render(self, name, value, attrs=None):
        """
        Returns Google Map
        @param name:
        @param value:
        @param attrs:
        @return:
        """

        # Read geometry data from field
        try:
            location = GEOSGeometry(value)
        except Exception:
            # todo: geolocate user
            location = Point(-34.397, 150.644)

        # map div's id
        field_id = attrs.get('id')
        map_id = "%s_map_layer" % field_id

        # Set Google map's tag_attributes
        gmap_options = {
            'zoom': float(attrs.pop('zoom', 8)),
            'field_id': str(field_id),
            'map_id': str(map_id),
            'lat': location.x,
            'lon': location.y,
        }

        # Javascript to create GMap
        gmap_javascript = u"""
<script type="text/javascript">
    var opt = %s
</script>
""" % gmap_options

        attrs['id'] = map_id
        # Build attributed for GMap's div tag
        tag_attributes = self.build_attrs(attrs)
        # GMap's div tag
        tag = u"""
<div %s></div>
""" % flatatt(tag_attributes)

#        dialog = u"""
#<div id='dialog' title='Confirmation'>
#    <p>Delete marker?</p>
#</div>
#        """

        input = u'<input id="%(id)s" type="hidden" name="%(name)s" value="%(value)s" />' % {
            'id': field_id,
            'name': name,
            'value': location.wkt,
        }

        # Combine javascript with div tag with input tag
        res = mark_safe(gmap_javascript + tag + input)
        return res
