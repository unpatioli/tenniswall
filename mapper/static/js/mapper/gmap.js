$(function () {

    ///// Geolocation Start
    var initial_location;
    var browserSupportFlag = new Boolean();
    var newyork = new google.maps.LatLng(60, 105);
    var siberia = new google.maps.LatLng(40.69847032728747, -73.9514422416687);

    function geolocate(map) {
        // Try W3C Geolocation
        if (navigator.geolocation) {
            browserSupportFlag = true;
            navigator.geolocation.getCurrentPosition(
                    function(position) {
                        initial_location = new google.maps.LatLng(
                                position.coords.latitude,
                                position.coords.longitude
                        );
                        initMap(initial_location);
                    },
                    function () {
                        handleNoGeoLocation(browserSupportFlag, map);
                    }
            );
        } else {
            browserSupportFlag = false;
            handleNoGeoLocation(browserSupportFlag, map);
        }
    }

    function handleNoGeoLocation(errorFlag, map) {
        if (errorFlag) {
            alert("Geolocation service failed.");
            initial_location = newyork;
        } else {
            alert("Your browser doesn't support geolocation. We've placed you in Siberia.");
            initial_location = siberia;
        }
        initMap(initial_location);
    }
    ///// Geolocation End
    var map_id = opt['map_id']
    var myOptions = {
        zoom: opt['zoom'],
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById(map_id), myOptions);
    
    if (!opt['location'] || opt['location'] == 'geolocate') {
        geolocate(map);
    } else {
        var latlng = new google.maps.LatLng(
                opt['location']['lat'],
                opt['location']['lon']
        );
        initMap(latlng);
    }

    function initMap(position) {
        map.setCenter(position);
        createMarker(position);
    }

    function createMarker(position) {
        var marker = new google.maps.Marker({
            map: map,
            position: position,
            draggable: true
        });

        google.maps.event.addListener(map, 'click', function(event){
            placeMarker(event.latLng, marker);
        });

        google.maps.event.addListener(marker, 'position_changed', function(event){
            setFieldVal(marker);
        });

        setFieldVal(marker);
    }

    function setFieldVal(marker) {
        $("#debug").html(markerToWkt(marker));
        $("#id_location").val(markerToWkt(marker));
    }

    function placeMarker(location, marker) {
        marker.setPosition(location);
        marker.setMap(map);
    }

    function markerToWkt(marker) {
        var position = marker.get('position');
        return "POINT ("
                + position.lat()
                + " "
                + position.lng()
                + ")";
    }

});
