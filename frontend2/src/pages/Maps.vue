<template>
  <div id="wrapper">
    <!-- Display map section -->
    <div id="gmap" style="width: 100%; height: 1000px;"></div>

    <!-- Elements on map -->
    <div id="container-box">
      <div class="floating-box">
        <div class="glass">
          <div>
            <b-dropdown id="dropdown-1" text="Aurin Data" class="m-md-2">
              <b-dropdown-item >Age</b-dropdown-item>
              <b-dropdown-item >Salary</b-dropdown-item>
              <b-dropdown-item >Other languages</b-dropdown-item>
            </b-dropdown>

            <form class="example" style="margin:auto;max-width:300px">
              <input type="text" placeholder="Track user by ID.." name="search2">
              <button type="submit">Go</button>
            </form>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MainFooter from "@/layout/MainFooter";
import GoogleMapsApiLoader from "google-maps-api-loader";
export default {
  name: "maps-page",
  bodyClass: "maps-page",
  data: function() {
    return {
      min: Number.MAX_VALUE,
      max: -Number.MAX_VALUE,
    };
  },
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

      let incomeLayer = this.loadIncome(mapLayer);
      let earthquakeLayer = this.loadEarthquakeLayer();
      let mapLayer = this.loadMapLayer(map, incomeLayer);

      // adding layers into map
      mapLayer.setMap(map);
      earthquakeLayer.setMap(map);
    },

    loadMapLayer: function(map, incomeLayer) {
      let mapLayer = new google.maps.Data();
      mapLayer.loadGeoJson("./GeoJson-Data-master/SA3_2016_AUST_SIM.json", {
        idPropertyName: "SA3_CODE16",
      });
      mapLayer.setStyle((feature) => {
        let color = "white";
        let stroke_weight = 0.1;
        let stroke_opacity = 1;
        let fill_opacity = 0;

        /* display income attributes using gradient style */
        if (incomeLayer.getFeatureById(feature.getId())) {
          var high = [5, 69, 54];
          var low = [151, 83, 34];
          var delta =
            (feature.getProperty("income") - this.min) / (this.max - this.min);

          let colorA = [];
          for (var i = 0; i < 3; i++) {
            // calculate an integer color based on the delta
            colorA[i] = (high[i] - low[i]) * delta + low[i];
          }
          color =
            "hsl(" + colorA[0] + "," + colorA[1] + "%," + colorA[2] + "%)";
          console.log(delta, color);
          fill_opacity = 1;
        }


        // highlight when moveover
        if (feature.getProperty("isColorful") == true) {
          color = "yellow";
          stroke_weight = 2;
          fill_opacity = 1;
          stroke_opacity = 0.4;
        }

        // final style
        return {
          fillColor: color,
          fillOpacity: fill_opacity,
          strokeOpacity: stroke_opacity,
          strokeWeight: stroke_weight,
        };
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
      mapLayer.addListener("addfeature", (e) => {
        if (incomeLayer.getFeatureById(e.feature.getId())) {
          let income = incomeLayer
            .getFeatureById(e.feature.getId())
            .getProperty("est_p_inc_avg_tot_inc_excl_gov_pnsn_aud");
          e.feature.setProperty("income", income);
          if (income > this.max) {
            this.max = income;
          }
          if (income < this.min) {
            this.min = income;
          }
        }
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
    loadIncome: function() {
      let incomeLayer = new google.maps.Data();
      incomeLayer.loadGeoJson(
        "./GeoJson-Data-master/SA3_2016_Melb_Income.json",
        {
          idPropertyName: "sa3_code16",
        }
      );
      incomeLayer.loadGeoJson(
        "./GeoJson-Data-master/SA3_2016_Sydn_Income.json",
        {
          idPropertyName: "sa3_code16",
        }
      );
      return incomeLayer;
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

<style>
  #wrapper { position: relative; }

  #container-box { position: absolute; top: 250px; left: 30px; z-index: 99; }
  
  .floating-box {
    width: 400px;
    height: 400px;
    overflow: hidden;
  }

  .glass {
    width: 100%;
    height: 100%;
    left: 4px;
    top: 4px;
    background: rgba(40, 40, 40, 0);
    filter: blur(0px);
    z-index:999;
  }

  form.example input[type=text] {
    padding: 8px;
    font-size: 12px;
    border: 0px solid grey;
    float: left;
    width: 40%;
    background: black;
    margin-left: -29px;
  }

  form.example button {
    float: left;
    width: 15%;
    padding: 10px;
    background: black;
    color: white;
    font-size: 9.5px;
    border: 0px solid grey;
    border-left: none;
    cursor: pointer;
  }

  form.example button:hover {
    background:white;
    color: black;
  }

  form.example::after {
    content: "";
    clear: both;
    display: table;
  }
</style>