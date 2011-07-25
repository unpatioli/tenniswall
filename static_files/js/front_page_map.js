$(function(){
    var initial_location;
    var browserSupportFlag = new Boolean();
    var siberia = new google.maps.LatLng(60, 105);
    var newyork = new google.maps.LatLng(40.69847032728747, -73.9514422416687);

    function geolocate() {
        // Try W3C Geolocation
        if (navigator.geolocation) {
            browserSupportFlag = true;
            navigator.geolocation.getCurrentPosition(
                    // success
                    function(position) {
                        initial_location = new google.maps.LatLng(
                                position.coords.latitude,
                                position.coords.longitude
                        );
                        map.setCenter(initial_location);
                    },
                    
                    // error
                    function () {
                        handleNoGeoLocation(browserSupportFlag);
                    },

                    // options
                    { timeout: 2000 }
            );
        // Try Google Gears Geolocation
        } else if (google.gears) {
            browserSupportFlag = true;
            var geo = google.gears.factory.create('beta.geolocation');
            geo.getCurrentPosition(function(position) {
              initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
              map.setCenter(initialLocation);
            }, function() {
              handleNoGeoLocation(browserSupportFlag);
            });
        // Browser doesn't support geolocation
        } else {
            browserSupportFlag = false;
            handleNoGeoLocation(browserSupportFlag);
        }
    }

    function handleNoGeoLocation(errorFlag) {
        if (errorFlag) {
            // Geolocation service failed
            initial_location = newyork;
        } else {
            // Browser doesn't support geolocation
            initial_location = siberia;
        }
        map.setCenter(initial_location);
    }

    var map_id = "main_map";
    var map_div = $('<div></div>').attr({
        id: map_id
    });
    $("#content").append(map_div);

    var myOptions = {
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(map_div.get(0), myOptions);
    geolocate();

    var operaional_zoom = 7;
    var cluster = new MarkerClusterer(map);
    var max_markers_count = 10;

    function checkMarkerExists(coord) {
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

    function clearMarkers(bbox) {
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

    google.maps.event.addListener(map, 'idle', function(event){
        var bounds = map.getBounds();
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
            num: max_markers_count
        });

        clearMarkers(bounds);

        if (map.zoom >= operaional_zoom) {
            $.ajax({
                type: "POST",
                url: "walls/bbox.json/",
                data: json,
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    var markers = []
                    $.each(data, function(key, value) {
                        if (!checkMarkerExists(value)) {
                            var p = new google.maps.LatLng(value.lat, value.lng);
                            var m = new google.maps.Marker({
                                title: value.title,
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
    });
});
