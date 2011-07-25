$(function(){
    var map_id = "main_map";
    var map_div = $('<div></div>').attr({
        id: map_id
    });
    $("#content").append(map_div);

    var latlng = new google.maps.LatLng(50, 16);
    var myOptions = {
        zoom: 8,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById(map_id), myOptions);
    var markers = [];
    max_markers_count = 10;
    marker_threshold = max_markers_count * 3;
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

        $.ajax({
            type: "POST",
            url: "walls/bbox.json/",
            data: json,
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(data){
                if (markers.length > marker_threshold) {
                    $.each(markers, function(key, val){
                        val[0].setMap(null);
                        val = null;
                    });
                    markers = [];
                }
                $.each(data, function(key, value){
                    var m = new google.maps.Marker({
                        map: map,
                        title: value.title,
                        position: new google.maps.LatLng(value.lat, value.lng),
                        draggable: false
                    });
                    var i = new google.maps.InfoWindow({
                        content: value.info
                    });
                    google.maps.event.addListener(m, 'click', function(event){
                        i.open(map, m);
                    });
                    markers.push([m, i]);
                });
            }
        });
    });
}); 
