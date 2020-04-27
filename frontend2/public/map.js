function initMap() {
    // Styles a map in night mode.
    var map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: -25, lng: 130 },
      zoom: 4,
      disableDefaultUI: true,
      styles: [
        {
          elementType: "geometry",
          stylers: [
            {
              color: "#212121",
            },
          ],
        },
        {
          elementType: "labels.icon",
          stylers: [
            {
              visibility: "off",
            },
          ],
        },
        {
          elementType: "labels.text.fill",
          stylers: [
            {
              color: "#757575",
            },
          ],
        },
        {
          elementType: "labels.text.stroke",
          stylers: [
            {
              color: "#212121",
            },
          ],
        },
        {
          featureType: "administrative",
          elementType: "geometry",
          stylers: [
            {
              color: "#757575",
            },
            {
              visibility: "off",
            },
          ],
        },
        {
          featureType: "administrative.country",
          elementType: "labels.text.fill",
          stylers: [
            {
              color: "#9e9e9e",
            },
          ],
        },
        {
          featureType: "administrative.land_parcel",
          stylers: [
            {
              visibility: "off",
            },
          ],
        },
        {
          featureType: "administrative.locality",
          elementType: "labels.text.fill",
          stylers: [
            {
              color: "#bdbdbd",
            },
          ],
        },
        {
          featureType: "administrative.neighborhood",
          stylers: [
            {
              visibility: "off",
            },
          ],
        },
        {
          featureType: "poi",
          stylers: [
            {
              visibility: "off",
            },
          ],
        },
        {
          featureType: "poi",
          elementType: "labels.text",
          stylers: [
            {
              visibility: "off",
            },
          ],
        },
        {
          featureType: "poi",
          elementType: "labels.text.fill",
          stylers: [
            {
              color: "#757575",
            },
          ],
        },
        {
          featureType: "poi.park",
          elementType: "geometry",
          stylers: [
            {
              color: "#181818",
            },
          ],
        },
        {
          featureType: "poi.park",
          elementType: "labels.text.fill",
          stylers: [
            {
              color: "#616161",
            },
          ],
        },
        {
          featureType: "poi.park",
          elementType: "labels.text.stroke",
          stylers: [
            {
              color: "#1b1b1b",
            },
          ],
        },
        {
          featureType: "road",
          elementType: "geometry.fill",
          stylers: [
            {
              color: "#2c2c2c",
            },
          ],
        },
        {
          featureType: "road",
          elementType: "labels",
          stylers: [
            {
              visibility: "off",
            },
          ],
        },
        {
          featureType: "road",
          elementType: "labels.icon",
          stylers: [
            {
              visibility: "off",
            },
          ],
        },
        {
          featureType: "road",
          elementType: "labels.text.fill",
          stylers: [
            {
              color: "#8a8a8a",
            },
          ],
        },
        {
          featureType: "road.arterial",
          elementType: "geometry",
          stylers: [
            {
              color: "#373737",
            },
          ],
        },
        {
          featureType: "road.highway",
          elementType: "geometry",
          stylers: [
            {
              color: "#3c3c3c",
            },
          ],
        },
        {
          featureType: "road.highway.controlled_access",
          elementType: "geometry",
          stylers: [
            {
              color: "#4e4e4e",
            },
          ],
        },
        {
          featureType: "road.local",
          elementType: "labels.text.fill",
          stylers: [
            {
              color: "#616161",
            },
          ],
        },
        {
          featureType: "transit",
          stylers: [
            {
              visibility: "off",
            },
          ],
        },
        {
          featureType: "transit",
          elementType: "labels.text.fill",
          stylers: [
            {
              color: "#757575",
            },
          ],
        },
        {
          featureType: "water",
          elementType: "geometry",
          stylers: [
            {
              color: "#000000",
            },
          ],
        },
        {
          featureType: "water",
          elementType: "labels.text",
          stylers: [
            {
              visibility: "off",
            },
          ],
        },
        {
          featureType: "water",
          elementType: "labels.text.fill",
          stylers: [
            {
              color: "#3d3d3d",
            },
          ],
        },
      ],
    });
    console.log('before load json');
    map.data.loadGeoJson('./GeoJson-Data-master/australian-states.json');
    console.log('after load json');
    
    //   map.mapTypes.set('myStyle', myStyle);
    //   map.setMapTypeId('myStyle');
  
    //   map.data.setStyle((feature) => ({
    //     fillColor: "red",
    //   }));
  
    // auto zoom after click one region
    map.data.addListener("click", function (e) {
      bounds = new google.maps.LatLngBounds();
  
      e.feature.getGeometry().forEachLatLng((x) => bounds.extend(x));
      map.fitBounds(bounds);
      map.panToBounds(bounds);
  
      // if (e.feature.getId()===1) {
      //   console.log('VIC');
      //   map.data.loadGeoJson("GeoJson-Data-master/melbourne.geojson");
      //   console.log(map.data);
      // }
      // console.log(map.getZoom());
    });
  
    map.data.addListener("mouseover", (e) => {
      map.data.revertStyle();
      map.data.overrideStyle(e.feature, { fillColor: "white" });
    });
  
    map.data.addListener("mouseout", (e) => {
      map.data.revertStyle();
    });
  
    map.addListener("zoom_changed", () => {
        console.log(map.getZoom());
    });
  }