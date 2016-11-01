if ($('#map').length) {
  var VAM = {
    map: {
      instance: {},
      geocoder: {},
      marker: {},
      openedInfoWindow: undefined,
      addMarker: function (options) {
        var marker = new google.maps.Marker({
          map: VAM.map.instance,
          title: options.title,
          position: {lat: options.lat, lng: options.lng},
          icon: options.icon
        });


        var content = options.content;
        var infoWindow = new google.maps.InfoWindow();

        google.maps.event.addListener(marker, 'click', (function (marker, content, infowindow) {
          return function () {
            if (VAM.map.openedInfoWindow !== undefined) {
              VAM.map.openedInfoWindow.close();
            }
            VAM.map.openedInfoWindow = infowindow;
            infowindow.setContent(content);
            infowindow.open(VAM.map.instance, marker);
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
      {%
        if search %}
      this.handleSearch('{{ search }}');
      {%
        endif %
      }
    },
    getMapData: function () {
      $.getJSON('{{ map_data_url }}', function (data) {
        $.each(data, function (index, value) {
          if (!value.address.latitude && !value.address.longitude) {
            return;
          }

          VAM.objects[value.id] = value;
          options = {
            title: value.name,
            lat: Number(value.address.latitude),
            lng: Number(value.address.longitude),
            content: VAM.getInfoWindowContent(value),
            icon: VAM.getIcon(value)
          };

          VAM.map.addMarker(options);
        });
      })
    },
    handleSearch: function (search) {
      if (search === undefined) {
        if ($('#map-search').val() != '') {
          search = $('#map-search').val();
          // some dirty code to change the url without refresh (making the searchresults when clicking the searchbutton on mapshareable)
          window.history.pushState({}, '', window.location.origin + window.location.pathname + '?search=' + search);
        } else {
          return;
        }
      }

      VAM.map.geocoder.geocode({'address': search}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          var location = results[0].geometry.location;
          VAM.map.instance.setCenter(location);
          VAM.map.instance.setZoom(15);
        } else {
          console.log('Something went wrong with Geocoder:', results, status);
        }
      })
    },
    getInfoWindowContent: function (value) {
      var content = '';

      content += '<div class="infowindow">';

      content += '<h2>' + value.name + '</h2>';

      if (value.opening_time) {
        content += '<h4>' + 'Öffnungszeiten' + '</h4>';
        content += '<p>' + value.opening_time + '</p>';
      }

      if (value.pickup) {
        content += '<h4>' + 'Abholservice' + '</h4>';
        content += '<p>' + value.pickup_description + '</p>';
      }


      if (value.notes) {
        content += '<h4>' + 'Weitere Informationen' + '</h4>';
        content += '<p>' + value.notes + '</p>';
      }

      if (value.sbb) {
        content += '<p><a href="#">' + 'SBB Transporteticket bestellen' + '</a></p>';
      }

      content += '</div>';

      return content;
    },
    getIcon: function (value) {
      var icon = 'img/map-icons/default.png';
      if (value.temp) {
        icon = 'img/map-icons/temp.png';
      }

      if (value.pickup) {
        icon = 'img/map-icons/pickup.png';
      }
      return icon;
    }
  };
}
