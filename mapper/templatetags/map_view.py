from django import template

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
