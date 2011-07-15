$(function () {
    var latlng = new google.maps.LatLng(opt['lat'], opt['lon']);
    var map_id = opt['map_id']
    var myOptions = {
        zoom: opt['zoom'],
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById(map_id), myOptions);
    var marker = new google.maps.Marker({
        map: map,
        position: latlng,
        draggable: true
    });

    google.maps.event.addListener(map, 'click', function(event){
        placeMarker(event.latLng);
    });

    google.maps.event.addListener(marker, 'position_changed', function(event){
        $("#debug").html(markerToWkt());
        $("#id_location").val(markerToWkt());
    });

    function placeMarker(location) {
        marker.setPosition(location);
        marker.setMap(map);
//        google.maps.event.addListener(marker, 'click', function(event){
//            $("#dialog").dialog('open');
//        });

//        map.setCenter(location);
    }

    function markerToWkt() {
        var position = marker.get('position');
        return "POINT ("
                + position.lat()
                + " "
                + position.lng()
                + ")";
    }

    $("#dialog").dialog({
        autoOpen: false,
        resizable: false,
        modal: true,
        buttons: {
            "Yes": function() {
                marker.setMap(null);
                $(this).dialog('close');
            },
            "No": function() {
                $(this).dialog('close');
            }
        }
    });

});
