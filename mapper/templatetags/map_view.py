from django import template
from django.utils.safestring import SafeUnicode
import settings

register = template.Library()

@register.simple_tag
def map_view(wall, zoom='8', width='1000px', height='500px'):
    """
    Inserts google map widget with wall, marked on it
    !!! Needs GoogleMaps API and JQuery to be included !!!
    """
    tag = """
<script type="text/javascript">
$(function() {
    var latlng = new google.maps.LatLng(%(lat)s, %(lon)s);
    var map_id = '%(map_id)s';
    var myOptions = {
        zoom: %(zoom)s,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById(map_id), myOptions);
    var marker = new google.maps.Marker({
        map: map,
        position: latlng,
        draggable: false
    });

    google.maps.event.addListener(marker, 'click', function(event){
        resetMap();
    });

    var loc = $("#locate_marker_control");
    if (loc) {
        var loc_html = loc.html();
        loc.html('<a href="" id="locate_marker_control_href">' + loc_html + '</a>');
        $("#locate_marker_control_href").click(function(event) {
            resetMap();
            return false;
        });
    }

    function resetMap() {
        map.setCenter(latlng);
        map.setZoom(%(zoom)s);
    }
});
</script>

<div id='%(map_id)s' style="width: %(width)s; height: %(height)s;">
</div>
    """ % {
        'map_id': "map_" + str(wall.pk),
        'lat': str(wall.location.x),
        'lon': str(wall.location.y),
        'zoom': float(zoom),
        'width': width,
        'height': height,
    }
    return tag

@register.simple_tag
def list_on_map(markers_url, wall_type, method='POST', data_type='json',
                content_type='application/json; charset=utf-8',
                zoom=8, operational_zoom=7, max_markers_count=10,
                width='', height='500px'):

    if wall_type[0] == '(' and wall_type[-1] == ')':
        wall_type = SafeUnicode('[' + wall_type[1:-1] + ']')
    elif not (wall_type[0] == '[' and wall_type[-1] == ']'):
        wall_type = '"%s"' % wall_type

    tag = """
<script type="text/javascript">
    var markers_url = "%(markers_url)s";
    var wall_type = %(wall_type)s;
    var method = "%(method)s";
    var data_type = "%(data_type)s";
    var content_type = "%(content_type)s";
    var zoom = %(zoom)s;
    var operational_zoom = %(operational_zoom)s;
    var max_markers_count = %(max_markers_count)i;
    var map_width = "%(width)s";
    var map_height = "%(height)s";

    var static_url = "%(STATIC_URL)s";
</script>
<script type="text/javascript" src="%(STATIC_URL)sjs/mapper/list_on_map.js"></script>
    """ % {
        'wall_type': wall_type,
        'markers_url': markers_url,
        'method': method,
        'data_type': data_type,
        'content_type': content_type,
        'zoom': zoom,
        'operational_zoom': operational_zoom,
        'max_markers_count': max_markers_count,
        'width': width,
        'height': height,
        'STATIC_URL': settings.STATIC_URL,
    }
    return tag
