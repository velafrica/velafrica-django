if ($('section.map').length) {
  $("#map-search").keyup(function(e){
    if (e.keyCode == 13 && $("#map-search").val() != '') {
      window.VAM.handleSearch($("#map-search").val());
    }
  });
  window.VAM = {
    data_url: '',
    sbb_ticket_order_url: $('#sbb-ticket-order-url').val(),
    map: {
      instance: {},
      geocoder: {},
      marker: {},
      openedInfoWindow: undefined,
      addMarker: function (options) {
        var marker = new google.maps.Marker({
          map: window.VAM.map.instance,
          title: options.title,
          position: {lat: options.lat, lng: options.lng},
          icon: options.icon
        });


        var content = options.content;
        var infoWindow = new google.maps.InfoWindow({'maxWidth': 400});

        google.maps.event.addListener(marker, 'click', (function (marker, content, infowindow) {
          return function () {
            if (window.VAM.map.openedInfoWindow !== undefined) {
              window.VAM.map.openedInfoWindow.close();
            }
            window.VAM.map.openedInfoWindow = infowindow;
            infowindow.setContent(content);
            infowindow.open(window.VAM.map.instance, marker);
            //TODO: center map to marker
          };
        })(marker, content, infoWindow));
      }
    },
    objects: {},
    initMap: function () {
      this.map.instance = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 46.798473, lng: 8.231726},
        zoom: 8,
        mapTypeControl: true,
        mapTypeControlOptions: {
          style: google.maps.MapTypeControlStyle.VERTICAL_BAR,
          position: google.maps.ControlPosition.TOP_RIGHT
        }
      });
      this.map.geocoder = new google.maps.Geocoder();
      this.getMapData();
      var search = window.getUrlVars()["search"];
      if (search) {
        this.handleSearch(decodeURIComponent(search));
      }

    },
    getMapData: function () {
      $.getJSON($('#map-data-url').val(), function (data) {
        $.each(data, function (index, value) {
          if (!value.address.latitude && !value.address.longitude) {
            return;
          }

          window.VAM.objects[value.id] = value;
          var options = {
            title: value.name,
            lat: Number((value.custom_lat) ? value.custom_lat : value.address.latitude),
            lng: Number((value.custom_lon) ? value.custom_lon : value.address.longitude),
            content: window.VAM.getInfoWindowContent(value),
            icon: window.VAM.getIcon(value)
          };

          window.VAM.map.addMarker(options);
        });
      })
    },
    handleSearch: function (search) {
      if (search === undefined) {
        if ($('#map-search').val() != '') {
          search = $('#map-search').val();
        } else {
          return;
        }
      }
      
      // some dirty code to change the url without refresh
      // (making the searchresults when clicking the searchbutton on map shareable)
      window.history.pushState({}, '', window.location.origin + window.location.pathname + '?search=' + search);

      $("#map-search").val(search);

      window.VAM.map.geocoder.geocode({'address': search + ', Schweiz', 'region': 'CH'}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          var location = results[0].geometry.location;
          window.VAM.map.instance.setCenter(location);
          window.VAM.map.instance.setZoom(15);
        } else {
          console.log('Something went wrong with Geocoder:', results, status);
        }
      })
    },
    getInfoWindowContent: function (value) {
      var content = '';

      content += '<div class="infowindow">';
      content += '<div class="container" style="max-width: 100%;">';

        content += '<div class="row">';
          content += '<h4 class="col-md-9" style="color: #E9571B; margin-bottom:0;">' + value.name + '</h4>';
          if ($('#auth').val() === 'True') {
            content += '<a target="_blank" class="col-md-3 btn btn-primary" href="/admin/collection/dropoff/' + value.id + '/change/">Bearbeiten</a>';
          }
        content += '</div>';

        content += '<div class="row">';
          content += '<p class="col-md-12 legend" style="padding-top:0;">' + value.address.street + '<br>' + value.address.zipcode + ' ' + value.address.city + '</p>';
        content += '</div>';

        if (value.opening_time) {
          content += '<div class="row">';
            content += '<div class="col-md-12">';
              content += '<h5 style="margin-bottom: 0;">Öffnungszeiten</h5>';
              content += '<p class="legend" style="padding-top:0;">' + value.opening_time + '</p>';
          content += '</div></div>';
        }

        if (value.pickup && value.pickup_description) {
          content += '<div class="row">';
            content += '<h5 class="col-md-12" style="margin-bottom: 0;">' + 'Abholservice' + '</h5>';
            content += '<p class="col-md-12 legend" style="padding-top: 0;">' + value.pickup_description + '</p>';
          content += '</div>';
        }

        if (value.notes) {
          content += '<div class="row">';
            content += '<h5 class="col-md-12" style="margin-bottom: 0;">' + 'Weitere Informationen' + '</h5>';
            content += '<p class="col-md-12 legend" style="padding-top: 0;">' + value.notes + '</p>';
          content += '</div>';
        }

        if (value.sbb) {
          content += '<div class="row">';
            content += '<a target="_blank" class="col-md-12 legend" href="' + window.VAM.sbb_ticket_order_url +'?id=' + value.id + '">' + 'SBB-Transportetikette bestellen' + '</a>';
          content += '</div>';
        }

      if(value.temp_start && value.temp_end) {
        content += '<p class="lead">Temporär von ' + value.temp_start + ' bis ' + value.temp_end + '</p>';
      }


      content += '</div></div>';

      return content;
    },
    getIcon: function (value) {
      var icon = '/static/img/map-icons/default.png';
      if (value.temp) {
        icon = '/static/img/map-icons/temp.png';
      }

      if (value.pickup) {
        icon = '/static/img/map-icons/pickup.png';
      }
      return icon;
    }
  };

  // load the map
  setTimeout(function(){
    window.VAM.initMap();
  }, 2000);
}
