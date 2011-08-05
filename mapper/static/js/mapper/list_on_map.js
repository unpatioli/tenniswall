$(function() {
    // Geolocation
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
    // End geolocation

    $(
    '<div id="wall_types_select_bar" class="span-24 last">' +
        '<input type="checkbox" checked="1" id="wall_type_free" class="toggle" />' +
        '<label for="wall_type_free" class="toggle">Free</label>' +

        '<input type="checkbox" checked="1" id="wall_type_paid" class="toggle" />' +
        '<label for="wall_type_paid" class="toggle">Paid</label> '
    ).appendTo("#content");
    $("#wall_types_select_bar").buttonset();

    var map_id = "main_map";
    var map_div = $('<div></div>').attr({
        id: map_id,
        class: "span-24 last",
        style: "width:" + map_width + ";" +
                "height:" + map_height
    });
    $("#content").append(map_div);

    var myOptions = {
        zoom: zoom,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(map_div.get(0), myOptions);
    geolocate();
    
    var cluster = new MarkerClusterer(map);

    google.maps.event.addListener(map, 'idle', function(event){
        mapRedraw(map, wall_type, cluster);
    });

    $("#wall_type_free").
    add("#wall_type_paid").
            change(function() {
                mapChangeRedraw();
            });

    function mapChangeRedraw() {
        var wt = [];
        if ($("#wall_type_free").is(':checked')) {
            wt.push('free');
        }
        if ($("#wall_type_paid").is(':checked')) {
            wt.push('paid');
        }
        
        mapRedraw(map, wt, cluster, true);
    }
});
