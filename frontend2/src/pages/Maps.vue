<template>
  <div>
    <div id="gmap" style="width: 100%; height: 1000px;"></div>
  </div>
</template>

<script>
import MainFooter from "@/layout/MainFooter";
import GoogleMapsApiLoader from "google-maps-api-loader";
export default {
  name: "maps-page",
  bodyClass: "maps-page",
  methods: {
    initMap: function() {
      // Styles a map in night mode.
      var AUSSIE_BOUNDS = {
        north: -10,
        south: -44,
        west: 97,
        east: -188,
      };
      var map = new google.maps.Map(document.getElementById("gmap"), {
        center: { lat: -25, lng: 130 },
        restriction: {
          latLngBounds: AUSSIE_BOUNDS,
          strictBounds: false,
        },
        zoom: 4,
        disableDefaultUI: true,
        disableDoubleClickZoom: true,
        styles: [
          {
            elementType: "geometry",
            stylers: [
              {
                color: "#f5f5f5",
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
                color: "#616161",
              },
            ],
          },
          {
            elementType: "labels.text.stroke",
            stylers: [
              {
                color: "#f5f5f5",
              },
            ],
          },
          {
            featureType: "administrative.land_parcel",
            elementType: "labels.text.fill",
            stylers: [
              {
                color: "#bdbdbd",
              },
            ],
          },
          {
            featureType: "poi",
            elementType: "geometry",
            stylers: [
              {
                color: "#eeeeee",
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
                color: "#e5e5e5",
              },
            ],
          },
          {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [
              {
                color: "#9e9e9e",
              },
            ],
          },
          {
            featureType: "road",
            elementType: "geometry",
            stylers: [
              {
                color: "#ffffff",
              },
            ],
          },
          {
            featureType: "road.arterial",
            elementType: "labels.text.fill",
            stylers: [
              {
                color: "#757575",
              },
            ],
          },
          {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [
              {
                color: "#dadada",
              },
            ],
          },
          {
            featureType: "road.highway",
            elementType: "labels.text.fill",
            stylers: [
              {
                color: "#616161",
              },
            ],
          },
          {
            featureType: "road.local",
            elementType: "labels.text.fill",
            stylers: [
              {
                color: "#9e9e9e",
              },
            ],
          },
          {
            featureType: "transit.line",
            elementType: "geometry",
            stylers: [
              {
                color: "#e5e5e5",
              },
            ],
          },
          {
            featureType: "transit.station",
            elementType: "geometry",
            stylers: [
              {
                color: "#eeeeee",
              },
            ],
          },
          {
            featureType: "water",
            elementType: "geometry",
            stylers: [
              {
                color: "#c9c9c9",
              },
            ],
          },
          {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [
              {
                color: "#9e9e9e",
              },
            ],
          },
        ],
      });

      let mapLayer = this.loadMapLayer(map);
      let earthquakeLayer = this.loadEarthquakeLayer();
      // adding layers into map
      mapLayer.setMap(map);
      earthquakeLayer.setMap(map);
    },

    loadMapLayer: function(map) {
      let mapLayer = new google.maps.Data();
      mapLayer.loadGeoJson("./GeoJson-Data-master/SA3_2016_AUST_SIM.json", {
        idPropertyName: "isColorful",
      });
      mapLayer.setStyle((feature) => {
        if (feature.getProperty("isColorful")) {
          let color = "yellow";
          return {
            fillColor: color,
            strokeOpacity: 2,
          };
        } else {
          return {
            //strokeOpacity:0,
            fillOpacity: 0,
            strokeWeight: 0.1,
          };
        }
      });

      // auto zoom after click one region
      mapLayer.addListener("rightclick", (e) => {
        var maker = new google.maps.Marker({
          position: e.latLng,
          map: map,
        });
      });
      mapLayer.addListener("dblclick", function(e) {
        let bounds = new google.maps.LatLngBounds();
        e.feature.getGeometry().forEachLatLng((x) => bounds.extend(x));
        map.fitBounds(bounds);
        map.panToBounds(bounds);
      });
      mapLayer.addListener("mouseover", (e) => {
        e.feature.setProperty("isColorful", true);
      });
      mapLayer.addListener("mouseout", (e) => {
        e.feature.setProperty("isColorful", false);
      });

      return mapLayer;
    },

    loadEarthquakeLayer: function() {
      let earthquakeLayer = new google.maps.Data();
      earthquakeLayer.loadGeoJson("./GeoJson-Data-master/earthquakes.geojson");
      earthquakeLayer.setStyle((feature) => {
        // earthquake circle
        let mag = feature.getProperty("mag");
        var circleMarker = {
          path: google.maps.SymbolPath.CIRCLE,
          fillColor: "red",
          fillOpacity: 0.4,
          scale: Math.pow(2, mag) / 2,
          strokeColor: "white",
          strokeWeight: 0.5,
        };
        // highlight states white when mouseover
        return {
          icon: circleMarker,
        };
      });
      return earthquakeLayer;
    },
  },
  mounted() {
    const googleMapApi = GoogleMapsApiLoader({
      apiKey: "AIzaSyDXG60896YH8pjO-svO4f7zQlxWBlZHp98",
    }).then((google) => {
      this.google = googleMapApi;
      this.initMap();
    });
  },
};
</script>

<style></style>
