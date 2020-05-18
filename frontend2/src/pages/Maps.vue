<template>
  <div id="wrapper">
    <!-- Display map section -->
    <div id="gmap" style="width: 100%; height: 1000px;"></div>

    <!-- Elements on map -->

    <div>
      <b-button id="side-button" v-b-toggle.sidebar-variant
        >Display options</b-button
      >
      <b-sidebar
        id="sidebar-variant"
        title="Display options"
        bg-variant="dark"
        text-variant="light"
        shadow
      >
        <div class="px-3 py-2">
          <b-img
            src="https://picsum.photos/500/500/?image=54"
            fluid
            thumbnail
          ></b-img>
        </div>
        <div id="container-box">
          <div class="floating-box">
            <div class="glass">
              <div>
                <b-dropdown id="dropdown-1" text="Aurin Data">
                  <b-dropdown-item>Age</b-dropdown-item>
                  <b-dropdown-item>Salary</b-dropdown-item>
                  <b-dropdown-item>Other languages</b-dropdown-item>
                  <b-dropdown-item @click="displayIncome"
                    >Income</b-dropdown-item
                  >
                  <b-dropdown-item @click="displayPopulation"
                    >Population</b-dropdown-item
                  >
                  <b-dropdown-item @click="zoomToMelb"
                    >Melbourne</b-dropdown-item
                  >
                  <b-dropdown-item @click="loadTwitterCount"
                    >Tweets</b-dropdown-item
                  >
                  <b-dropdown-item @click="hideTwitterCount"
                    >Hide Tweets</b-dropdown-item
                  >
                </b-dropdown>
              </div>
              <div>
                <form class="example">
                  <input
                    type="text"
                    placeholder="Track user by ID.."
                    name="search2"
                  />
                  <button type="submit">Go</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </b-sidebar>
    </div>
    <div id="SA3-info" v-if="displayCard">
      <b-card
        bg-variant="dark"
        header="Area info"
        text-variant="white"
        class="text-center"
      >
        <b-card-text>Area: {{ sa3_name }}</b-card-text>
        <b-card-text>Mean income: {{ sa3_mean_income }}</b-card-text>
        <b-card-text>Total population: {{ sa3_total_population }}</b-card-text>
      </b-card>
    </div>
  </div>
</template>

<script>
import MainFooter from "@/layout/MainFooter";
import GoogleMapsApiLoader from "google-maps-api-loader";
import tweetCount from "../../public/GeoJson-Data-master/count.json";
export default {
  name: "maps-page",
  bodyClass: "maps-page",
  data: function() {
    return {
      map: null,
      mapLayer: null,
      markers: [],
      displayOption: "income",
      displayCard: false,
      sa3_name: null,
      sa3_mean_income: null,
      sa3_total_population:null,
      incomeMin: Number.MAX_VALUE,
      incomeMax: -Number.MAX_VALUE,
      populationMin: Number.MAX_VALUE,
      populationMax: -Number.MAX_VALUE,
      tweetMin: Number.MAX_VALUE,
      tweetMax: -Number.MAX_VALUE,
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
      this.map = new google.maps.Map(document.getElementById("gmap"), {
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
      let incomeLayer = this.loadIncome();
      let populationLayer = this.loadPopulation();
      this.mapLayer = this.loadMapLayer(incomeLayer, populationLayer);
      // adding layers into map
      this.mapLayer.setMap(this.map);
    },
    loadMapLayer: function(incomeLayer, populationLayer) {
      let maplayer = new google.maps.Data();
      maplayer.loadGeoJson("./GeoJson-Data-master/SA3_2016_AUST_SIM.json", {
        idPropertyName: "SA3_CODE16",
      });
      maplayer.setStyle((feature) => {
        let color = "white";
        let stroke_weight = 0.1;
        let stroke_opacity = 1;
        let fill_opacity = 0;
        /* display income attributes using gradient style */
        if (
          feature.getProperty("displayOption") == "income" &&
          incomeLayer.getFeatureById(feature.getId())
        ) {
          var high = [5, 69, 54];
          var low = [151, 83, 34];
          var delta =
            (feature.getProperty("income") - this.incomeMin) /
            (this.incomeMax - this.incomeMin);
          let colorA = [];
          for (var i = 0; i < 3; i++) {
            // calculate an integer color based on the delta
            colorA[i] = (high[i] - low[i]) * delta + low[i];
          }
          color =
            "hsl(" + colorA[0] + "," + colorA[1] + "%," + colorA[2] + "%)";
          fill_opacity = 0.5;
        }
        /* population */
        if (
          feature.getProperty("displayOption") == "population" &&
          populationLayer.getFeatureById(feature.getId())
        ) {
          var high = [5, 69, 54];
          var low = [151, 83, 34];
          var delta =
            (feature.getProperty("population") - this.populationMin) /
            (this.populationMax - this.populationMin);
          let colorA = [];
          for (var i = 0; i < 3; i++) {
            // calculate an integer color based on the delta
            colorA[i] = (high[i] - low[i]) * delta + low[i];
          }
          color =
            "hsl(" + colorA[0] + "," + colorA[1] + "%," + colorA[2] + "%)";
          fill_opacity = 0.5;
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
      maplayer.addListener("rightclick", (e) => {
        var maker = new google.maps.Marker({
          position: e.latLng,
          map: this.map,
        });
      });
      maplayer.addListener("dblclick", function(e) {
        let bounds = new google.maps.LatLngBounds();
        e.feature.getGeometry().forEachLatLng((x) => bounds.extend(x));
        this.map.fitBounds(bounds);
        this.map.panToBounds(bounds);
      });
      maplayer.addListener("mouseover", (e) => {
        this.displayCard = true;
        this.sa3_name = e.feature.getProperty("SA3_NAME16");
        this.sa3_total_population = e.feature.getProperty("population");
        this.sa3_mean_income = e.feature.getProperty("income");
        e.feature.setProperty("isColorful", true);
      });
      maplayer.addListener("mouseout", (e) => {
        this.displayCard = false;
        e.feature.setProperty("isColorful", false);
      });
      maplayer.addListener("addfeature", (e) => {
        if (incomeLayer.getFeatureById(e.feature.getId())) {
          let income = incomeLayer
            .getFeatureById(e.feature.getId())
            .getProperty("est_p_inc_avg_tot_inc_excl_gov_pnsn_aud");
          e.feature.setProperty("income", income);
          if (income > this.incomeMax) {
            this.incomeMax = income;
          }
          if (income < this.incomeMin) {
            this.incomeMin = income;
          }
        }
        if (populationLayer.getFeatureById(e.feature.getId())) {
          let population = populationLayer
            .getFeatureById(e.feature.getId())
            .getProperty("persons_total");
          e.feature.setProperty("population", population);
          if (population > this.populationMax) {
            this.populationMax = population;
          }
          if (population < this.populationMin) {
            this.populationMin = population;
          }
        }
      });
      return maplayer;
    },
    loadTwitterCount: function() {
      this.markers = [];
      for (var key in tweetCount) {
        if (tweetCount[key] > this.tweetMax) {
          this.tweetMax = tweetCount[key];
        }
        if (tweetCount[key] < this.tweetMin) {
          this.tweetMin = tweetCount[key];
        }
      }
      for (var key in tweetCount) {
        let feature = this.mapLayer.getFeatureById(key);
        let bounds = new google.maps.LatLngBounds();
        feature.getGeometry().forEachLatLng((x) => bounds.extend(x));
        let center = bounds.getCenter();
        let size =
          ((tweetCount[key] - this.tweetMin) /
            (this.tweetMax - this.tweetMin)) *
          50;
        let circleMarker = {
          position: center,
          path: google.maps.SymbolPath.CIRCLE,
          fillColor: "red",
          fillOpacity: 0.4,
          scale: size,
          strokeColor: "white",
          strokeWeight: 0.5,
        };
        console.log("size:", size);
        var marker = new google.maps.Marker({
          position: center,
          icon: circleMarker,
        });
        this.markers.push(marker);
      }
      for (let i = 0; i < this.markers.length; i++) {
        this.markers[i].setMap(this.map);
      }
    },
    hideTwitterCount: function() {
      for (let i = 0; i < this.markers.length; i++) {
        this.markers[i].setMap(null);
      }
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
    loadPopulation: function() {
      let populationLayer = new google.maps.Data();
      populationLayer.loadGeoJson(
        "./GeoJson-Data-master/SA3_2017_Melb_Population.json",
        {
          idPropertyName: "sa3_code16",
        }
      );
      populationLayer.loadGeoJson(
        "./GeoJson-Data-master/SA3_2017_Sydn_Population.json",
        {
          idPropertyName: "sa3_code16",
        }
      );
      return populationLayer;
    },
    zoomToMelb: function() {
      var myOptions = {
        zoom: 9,
        center: new google.maps.LatLng(-37.815018, 144.946014),
        panControl: false,
      };
      this.map.setOptions(myOptions);
    },
    displayIncome: function() {
      this.mapLayer.forEach(function(feature) {
        feature.setProperty("displayOption", "income");
      });
    },
    displayPopulation: function() {
      this.mapLayer.forEach(function(feature) {
        feature.setProperty("displayOption", "population");
      });
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
#wrapper {
  position: relative;
}
#container-box {
  position: absolute;
  top: 350px;
  left: 30px;
  z-index: 99;
}
#side-button {
  position: absolute;
  top: 150px;
  left: 350px;
}
#SA3-info {
  position: absolute;
  top: 250px;
  right: 30px;
  width: 250px;
}
.floating-box {
  width: 300px;
  height: 500px;
  overflow: hidden;
}
.glass {
  margin-left: 0px;
  width: 100%;
  height: 100%;
  left: 4px;
  top: 4px;
  background: rgba(40, 40, 40, 0);
  filter: blur(0px);
  z-index: 999;
}
form.example {
  margin-left: 0px;
}
form.example input[type="text"] {
  padding: 8px;
  font-size: 12px;
  color: white;
  border: 0px solid grey;
  float: left;
  width: 40%;
  background: black;
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
  background: white;
  color: black;
}
form.example::after {
  content: "";
  clear: both;
  display: table;
}
</style>