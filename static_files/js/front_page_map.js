$(function(){
    var map_id = "main_map";
    var map_div = $('<div></div>').attr({
        id: map_id
    });
    $("#content").append(map_div);

    var debug = $('<div></div>')
    $("#content").append(debug);

    var latlng = new google.maps.LatLng(50, 16);
    var myOptions = {
        zoom: 8,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(map_div.get(0), myOptions);
    var markers = [];
    var max_markers_count = 10;
    var marker_threshold = max_markers_count * 3;
    var fluster = new Fluster2(map);

    function checkMarker(coord) {
        for (var i = 0; i < fluster.markers.length; ++i) {
            var val = fluster.markers[i];
            if (coord.lat == val.position.lat() &&
                    coord.lng == val.position.lng()) {
                return true;
            }
        };
        return false;
    }

    function clearMarkers(bbox) {
        for (var i = 0; i < fluster.markers.length; ++i) {
            var val = fluster.markers[i];
            if (!bbox.contains(val.position)) {
                fluster.markers[i].setMap(null);
                fluster.markers[i] = null;
                fluster.markers.splice(i,1);
                i--;
            }
        }
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

        // DEBUG
        debug.html("Count: " + fluster.markers.length);
        // END DEBUG

        $.ajax({
            type: "POST",
            url: "walls/bbox.json/",
            data: json,
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(data){
//                if (markers.length > marker_threshold) {
//                    $.each(markers, function(key, val){
//                        val[0].setMap(null);
//                        val[0] = null;
//                        val[1] = null;
//                    });
//                    markers = [];
//                }
                
                $.each(data, function(key, value){
                    if (!checkMarker(value)) {
                        var p = new google.maps.LatLng(value.lat, value.lng);
                        var m = new google.maps.Marker({
    //                        map: map,
                            title: value.title,
                            position: p,
                            draggable: false
                        });
                        var i = new google.maps.InfoWindow({
                            content: value.info
                        });
                        google.maps.event.addListener(m, 'click', function(event){
                            i.open(map, m);
                        });
                        fluster.addMarker(m);
//                        markers.push([m, i]);
                    }
                });
            }
        });
    });
    fluster.initialize();
}); 
