function clearMarkers(bbox, cluster) {
    markers = cluster.getMarkers();
    var markers_to_remove = [];
    for (var i = 0; i < markers.length; ++i) {
        var val = markers[i];
        if (!bbox.contains(val.position)) {
            markers_to_remove.push(val);
        }
    }
    cluster.removeMarkers(markers_to_remove);
}

function checkMarkerExists(coord, cluster) {
    var markers = cluster.getMarkers();
    for (var i = 0; i < markers.length; ++i) {
        var marker = markers[i];
        if (coord.lat == marker.position.lat() &&
                coord.lng == marker.position.lng()) {
            return true;
        }
    }
    return false;
}

function mapRedraw(map, wall_type, cluster, purge) {
    var bounds = map.getBounds();
    if (purge) {
        cluster.clearMarkers();
    } else {
        clearMarkers(bounds, cluster);
    }

    if (map.zoom >= operational_zoom) {

        var ne = bounds.getNorthEast();
        var sw = bounds.getSouthWest();

        var json = $.toJSON({
            ne: {
                lat: ne.lat(),
                lng: ne.lng()
            },
            sw: {
                lat: sw.lat(),
                lng: sw.lng()
            },
            num: max_markers_count,
            wall_type: wall_type
        });
        
        $.ajax({
            type: method,
            url: markers_url,
            data: json,
            dataType: data_type,
            contentType: content_type,
            success: function(data) {
                var markers = []
                $.each(data, function(key, value) {
                    if (!checkMarkerExists(value, cluster)) {
                        var p = new google.maps.LatLng(value.lat, value.lng);
                        if (value.is_paid) {
                            var img = new google.maps.MarkerImage(static_url + 'img/icons/map/tennis.png');
                        } else {
                            var img = new google.maps.MarkerImage(static_url + 'img/icons/map/tennis2.png');
                        }
                        var m = new google.maps.Marker({
                            title: value.title,
                            flat: true,
                            icon: img,
                            position: p,
                            draggable: false
                        });
                        var content = value.info +
                                '<br/>' +
                                '<a href="' + value.url + '">'
                                    + value.link_title +
                                '</a>';
                        var i = new google.maps.InfoWindow({
                            content: content
                        });
                        google.maps.event.addListener(m, 'click', function(event) {
                            i.open(map, m);
                        });
                        markers.push(m);
                    }
                });
                cluster.addMarkers(markers);
            }
        });
    }
}
