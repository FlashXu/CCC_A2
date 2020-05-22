<template>
  <div id="wrapper">
    <!-- Display map section -->
    <div id="gmap" style="width: 100%; height: 1000px;"></div>

    <!-- Elements on map -->

    <div>
      <b-button id="side-button" v-b-toggle.sidebar-variant
        >Display options</b-button
      >

      <div class="tempbar">
        <div id="progress-bar-container">
          <div class="progress-bar-child progress"></div>
          <div class="progress-bar-child shrinker timelapse"></div>
        </div>

        <p id="text1">25,000</p>
        <p id="text2">Population</p>
        <p id="text3">300,000</p>

        <p id="text4">$50,000</p>
        <p id="text5">Income</p>
        <p id="text6">$150,000</p>
      </div>
      <div id="displayBar">
        <b-progress v-if="displayOption=='population'" :value="sa3_total_population" :max="populationMax" show-progress animated></b-progress>
        <b-progress v-if="displayOption=='income'" :value="sa3_mean_income" :max="incomeMax" show-progress animated></b-progress>
      </div>
      <b-sidebar
        id="sidebar-variant"
        title="Display options"
        bg-variant="dark"
        text-variant="light"
        shadow
      >
        <div id="container-box">
          <div class="floating-box">
            <div class="glass">
              <div>
                <b-dropdown id="dropdown-1" text="Aurin Data">
                  <!-- <b-dropdown-item>Age</b-dropdown-item>
                  <b-dropdown-item>Salary</b-dropdown-item>
                  <b-dropdown-item>Other languages</b-dropdown-item> -->
                  <b-dropdown-item @click="displayIncome"
                    >Income</b-dropdown-item
                  >
                  <b-dropdown-item @click="displayPopulation"
                    >Population</b-dropdown-item
                  >
                  <b-dropdown-item @click="displayTourism"
                    >Tourism</b-dropdown-item
                  >
                  <b-dropdown-item @click="hideDisplay"
                    >Hide Aurin Data</b-dropdown-item
                  >
                  <b-dropdown-item @click="zoomToMelb"
                    >Melbourne</b-dropdown-item
                  >
                  <b-dropdown-item @click="zoomToSydn">Sydney</b-dropdown-item>
                </b-dropdown>
              </div>

              <div>
                <b-dropdown id="dropdown-1" text="Twitter Data">
                  <b-dropdown-item @click="loadTwitterCount"
                    >Tweets</b-dropdown-item
                  >
                  <b-dropdown-item @click="hideTwitterCount"
                    >Hide Tweets</b-dropdown-item
                  >
                </b-dropdown>
              </div>

              <div>
                <button
                  type="submit"
                  id="changemode"
                  class="switchButton"
                  v-on:click="changeMode"
                >
                  Dynamic
                </button>
                <p class="modetext">Current Mode: {{ currentmode }}</p>
              </div>

              <div class="timesearch" v-if="currentmode == 'Dynamic'">
                <input
                  type="text"
                  id="starttime"
                  class="search_time"
                  placeholder="2014-01-23"
                />
                <p>~</p>
                <input
                  type="text"
                  id="endtime"
                  class="search_time"
                  placeholder="2018-09-10"
                />
                <button
                  type="submit"
                  class="searchtimeButton"
                  v-on:click="changeDate()"
                >
                  GO
                </button>
              </div>

              <div class="search">
                <input
                  type="text"
                  id="searchinput"
                  class="searchTerm"
                  placeholder="Please input SA3 code."
                  v-on:keyup.enter="godown"
                />
                <button type="submit" class="searchButton" v-on:click="godown">
                  GO
                </button>
              </div>

              <div class="chartoptions">
                <button class="linechartBtn" v-on:click="goLine">
                  <a id="premium">Line</a>
                </button>
                <button class="piechartBtn" v-on:click="goPie">
                  <a id="premium">Pie</a>
                </button>
                <button class="barchartBtn" v-on:click="goBar">
                  <a id="premium">Bar</a>
                </button>
                <button class="radarchartBtn" v-on:click="goRadar">
                  <a id="premium">Radar</a>
                </button>
                <button class="mixedBtn1" v-on:click="goMixed2">
                  <a id="premium">Tweets & Income </a>
                </button>
                <button class="mixedBtn2" v-on:click="goMixed1">
                  <a id="premium">Tweets & Age</a>
                </button>
                <b-img
                  id="sidebarpic"
                  src="https://picsum.photos/500/500/?image=54"
                  fluid
                  thumbnail
                ></b-img>
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
        <b-card-text>SA Code: {{ sa3_code }}</b-card-text>
        <b-card-text>Area: {{ sa3_name }}</b-card-text>
        <b-card-text v-if="sa3_total_population != null"
          >Total Population: {{ sa3_total_population }}</b-card-text
        >

        <div v-if="currentmode == 'Static'">
          <piechart
            v-if="popupcharttype == 'Pie'"
            :datapath="piedata"
            :sa3code="sa3_code"
          />
          <table v-if="iscontained" id="PopupTable">
            <tr>
              <th>Income(AUD$)</th>
              <th>Num of Tweets</th>
            </tr>
            <tr>
              <td>{{ sa3_mean_income }}</td>
              <td>{{ tweetcount }}</td>
            </tr>
          </table>
        </div>

        <div v-if="currentmode == 'Dynamic'">
          <barchart
            v-if="popupcharttype == 'godyn'"
            :datapath="currenttwt"
            :sa3code="sa3_code"
          />
          <table id="PopupTable" v-if="popupcharttype == 'godyn'">
            <tr>
              <th>Num of Tweets</th>
              <th>Num of En Tweets</th>
            </tr>
            <tr>
              <td>{{ currenttwt.twtnum }}</td>
              <td>{{ currenttwt.lang.en }}</td>
            </tr>
          </table>
        </div>
      </b-card>
    </div>

    <piechart
      class="piechart"
      v-if="charttype == 'Pie'"
      :datapath="piedata"
      :sa3code="sa3_code"
    />
    <linechart
      class="linechart"
      v-if="charttype == 'Line'"
      :datapath="linedata"
      :sa3code="sa3_code"
    />
    <barchart
      class="barchart"
      v-if="charttype == 'Bar'"
      :datapath="bardata"
      :sa3code="sa3_code"
    />
    <radarchart
      class="radarchart"
      v-if="charttype == 'Radar'"
      :datapath="radardata"
      :sa3code="sa3_code"
    />
    <mixedchart
      class="mixedchart"
      v-if="charttype == 'Mixed1'"
      :datapath="radardata"
      :sa3code="sa3_code"
      :tweetpath="twtpath"
      :mixedtype="charttype"
    />
    <mixedchart
      class="mixedchart"
      v-if="charttype == 'Mixed2'"
      :datapath="radardata"
      :sa3code="sa3_code"
      :tweetpath="twtpath"
      :mixedtype="charttype"
    />
  </div>
</template>

<script>
import MainFooter from "@/layout/MainFooter";
import GoogleMapsApiLoader from "google-maps-api-loader";
import tweetCount from "../../public/GeoJson-Data-master/count.json";
import datafile from "@/data/AURIN_data.json";
import piechart from "@/charttype/Piechart.vue";
import linechart from "@/charttype/Linechart.vue";
import barchart from "@/charttype/Barchart.vue";
import radarchart from "@/charttype/Radarchart.vue";
import mixedchart from "@/charttype/Mixedchart.vue";

export default {
  name: "maps-page",
  bodyClass: "maps-page",
  data: function() {
    return {
      map: null,
      mapLayer: null,
      tourismLayer:null,
      markers: [],
      displayOption: "null",
      displayCard: false,
      sa3_code: null,
      sa3_name: null,
      sa3_mean_income: null,
      sa3_total_population: null,
      incomeMin: Number.MAX_VALUE,
      incomeMax: -Number.MAX_VALUE,
      populationMin: Number.MAX_VALUE,
      populationMax: -Number.MAX_VALUE,
      tweetMin: Number.MAX_VALUE,
      tweetMax: -Number.MAX_VALUE,

      iscontained: false,
      tweetcount: 0,
      charttype: "null",
      popupcharttype: "null",
      piedata: datafile,
      linedata: datafile,
      bardata: datafile,
      radardata: datafile,
      mixeddata: datafile,
      mixedtype: "null",
      twtpath: tweetCount,

      currentmode: "Static",
      currenttwt: {},
    };
  },
  components: {
    piechart,
    linechart,
    barchart,
    radarchart,
    mixedchart,
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
        gestureHandling: "greedy",
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
      this.tourismLayer = this.loadTourism();
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
      maplayer.addListener("click", (e) => {
        this.displayCard = true;
        this.sa3_code = e.feature.getProperty("SA3_CODE16");
        this.sa3_name = e.feature.getProperty("SA3_NAME16");
        this.sa3_total_population = e.feature.getProperty("population");
        this.sa3_mean_income = e.feature.getProperty("income");
        this.tweetcount = tweetCount[this.sa3_code];
        e.feature.setProperty("isColorful", true);

        if (this.currentmode == "Static") {
          var currentsacode = document.getElementById("searchinput");
          var strs = currentsacode.value.toString().split(",");
          var changecode;
          if (strs.length == 1 && strs[0] == "") {
            if (datafile.hasOwnProperty(this.sa3_code)) {
              changecode = this.sa3_code;
              currentsacode.value = changecode;
            }
          } else {
            changecode = strs[0].trim();
            for (var i = 1; i < strs.length; i++) {
              changecode += "," + strs[i].trim();
            }
            if (datafile.hasOwnProperty(this.sa3_code)) {
              changecode += "," + this.sa3_code;
              currentsacode.value = changecode;
            }
          }
        }

        if (this.currentmode == "Dynamic") {
          var currentsacode = this.sa3_code;
          var nextmode = document.getElementById("changemode");
          if (nextmode.innerHTML == "Static") {
            var start_time = document
              .getElementById("starttime")
              .value.toString();
            if (start_time == "") {
              document.getElementById("starttime").value = "2014-01-23";
              start_time = "2014-01-23";
            }
            var end_time = document.getElementById("endtime").value.toString();
            if (end_time == "") {
              document.getElementById("endtime").value = "2018-09-10";
              end_time = "2018-09-10";
            }
            // 115.146.95.16   172.26.132.92   45.88.195.224
            var host = "115.146.95.16";
            var url1 = `http://${host}:5000/geo/${currentsacode}/${start_time}/${end_time}/`;
            var url2 = `http://${host}:5000/lang/${currentsacode}/${start_time}/${end_time}/`;

            const axios = require("axios");
            axios
              .all([axios.get(url1), axios.get(url2)])
              .then(
                axios.spread((r1, r2) => {
                  this.currenttwt = {};
                  this.currenttwt.twtnum = r1.data[currentsacode];
                  this.currenttwt.lang = r2.data[currentsacode];

                  this.popupcharttype = "null";
                  this.$nextTick(() => {
                    this.popupcharttype = "godyn";
                  });
                })
              )
              .catch((error) => {
                // console.log(error);
              });
          }
        }
      });
      maplayer.addListener("rightclick", (e) => {});
      maplayer.addListener("dblclick", function(e) {
        let bounds = new google.maps.LatLngBounds();
        e.feature.getGeometry().forEachLatLng((x) => bounds.extend(x));
        this.map.fitBounds(bounds);
        this.map.panToBounds(bounds);
      });
      maplayer.addListener("mouseover", (e) => {
        this.displayCard = true;
        this.sa3_code = e.feature.getProperty("SA3_CODE16");
        this.sa3_name = e.feature.getProperty("SA3_NAME16");
        this.sa3_total_population = e.feature.getProperty("population");
        this.sa3_mean_income = e.feature.getProperty("income");
        this.tweetcount = tweetCount[this.sa3_code];
        e.feature.setProperty("isColorful", true);

        if (this.currentmode == "Static") {
          if (datafile.hasOwnProperty(this.sa3_code)) {
            this.iscontained = false;
            this.popupcharttype = "null";

            this.$nextTick(() => {
              this.iscontained = true;
              this.popupcharttype = "Pie";
            });
          } else {
            this.iscontained = false;
            this.popupcharttype = "null";
          }
        }
      });
      maplayer.addListener("mouseout", (e) => {
        this.displayCard = false;
        e.feature.setProperty("isColorful", false);
        this.iscontained = false;
        this.popupcharttype = "null";
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
        // console.log("size:", size);
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
    loadTourism: function() {
      let tourismLayer = new google.maps.Data();
      tourismLayer.loadGeoJson("./GeoJson-Data-master/tourism.json", {
        idPropertyName: "tr_code14",
      });
      tourismLayer.setStyle((feature) => {
        let color = "white";
        let stroke_weight = 0.1;
        let stroke_opacity = 1;
        let fill_opacity = 0.3;

        if (feature.getProperty("rank") < 10) {
          color = "blue";
        }
        return {
          fillColor: color,
          fillOpacity: fill_opacity,
          strokeOpacity: stroke_opacity,
          strokeWeight: stroke_weight,
        };
      });
      return tourismLayer;
    },
    zoomToMelb: function() {
      var myOptions = {
        zoom: 9,
        center: new google.maps.LatLng(-37.815018, 144.946014),
        panControl: false,
      };
      this.map.setOptions(myOptions);
    },
    zoomToSydn: function() {
      var myOptions = {
        zoom: 9,
        center: new google.maps.LatLng(-33.856156, 151.004201),
        panControl: false,
      };
      this.map.setOptions(myOptions);
    },
    displayIncome: function() {
      this.mapLayer.forEach(function(feature) {
        feature.setProperty("displayOption", "income");
      });
      this.displayOption = "income";
      var myOptions = {
        zoom: 7,
        center: new google.maps.LatLng(-36.380542, 148.051793),
        panControl: false,
      };
      this.map.setOptions(myOptions);
    },
    displayTourism: function() {
      this.tourismLayer.setMap(this.map);
    },
    displayPopulation: function() {
      this.mapLayer.forEach(function(feature) {
        feature.setProperty("displayOption", "population");
      });
      this.displayOption = "population";
      var myOptions = {
        zoom: 7,
        center: new google.maps.LatLng(-36.380542, 148.051793),
        panControl: false,
      };
      this.map.setOptions(myOptions);
    },
    hideDisplay: function() {
      this.mapLayer.forEach(function(feature) {
        feature.setProperty("displayOption", "null");
      });
      this,displayOption = "null";
      this.tourismLayer.setMap(null);
    },
    goPie() {
      var searchbox = document.getElementById("searchinput");
      this.sa3_code = searchbox.value.toString();
      this.charttype = "null";
      this.$nextTick(() => {
        this.charttype = "Pie";
      });
    },
    goLine() {
      var searchbox = document.getElementById("searchinput");
      this.sa3_code = searchbox.value.toString();
      this.charttype = "null";
      this.$nextTick(() => {
        this.charttype = "Line";
      });
    },
    goBar() {
      var searchbox = document.getElementById("searchinput");
      this.sa3_code = searchbox.value.toString();
      this.charttype = "null";
      this.$nextTick(() => {
        this.charttype = "Bar";
      });
    },
    goRadar() {
      var searchbox = document.getElementById("searchinput");
      this.sa3_code = searchbox.value.toString();
      this.charttype = "null";
      this.$nextTick(() => {
        this.charttype = "Radar";
      });
    },
    goMixed1() {
      var searchbox = document.getElementById("searchinput");
      this.sa3_code = searchbox.value.toString();
      this.charttype = "null";
      this.$nextTick(() => {
        this.charttype = "Mixed1";
      });
    },
    goMixed2() {
      var searchbox = document.getElementById("searchinput");
      this.sa3_code = searchbox.value.toString();
      this.charttype = "null";
      this.$nextTick(() => {
        this.charttype = "Mixed2";
      });
    },
    changeMode() {
      var nextmode = document.getElementById("changemode");
      if (nextmode.innerHTML == "Dynamic") {
        nextmode.innerHTML = "Static";
        this.currentmode = "Dynamic";
      } else {
        nextmode.innerHTML = "Dynamic";
        this.currentmode = "Static";
      }
    },
    changeDate() {
      var start_time = document.getElementById("starttime").value.toString();
      if (start_time == "") {
        document.getElementById("starttime").value = "2014-01-23";
        start_time = "2014-01-23";
      }
      var end_time = document.getElementById("endtime").value.toString();
      if (end_time == "") {
        document.getElementById("endtime").value = "2018-09-10";
        end_time = "2018-09-10";
      }
    },
    godown() {
      var type = this.charttype;
      // if(type == "null"){
      //   alert("Please choose chart type first!");
      //   return;
      // }

      this.charttype = "null";

      this.$nextTick(() => {
        var searchbox = document.getElementById("searchinput");
        this.sa3_code = searchbox.value.toString();
        switch (type) {
          case "Pie":
          case "null":
            this.charttype = "Pie";
            break;
          case "Line":
            this.charttype = "Line";
            break;
          case "Bar":
            this.charttype = "Bar";
            break;
          case "Radar":
            this.charttype = "Radar";
            break;
          case "Mixed1":
            this.charttype = "Mixed1";
            break;
          case "Mixed2":
            this.charttype = "Mixed2";
            break;
        }
      });
      var scrollingElement = document.scrollingElement;
      scrollingElement.scrollTop = scrollingElement.scrollHeight;
    },
  },
  mounted() {
    this.charttype = "Pie";
    const googleMapApi = GoogleMapsApiLoader({
      apiKey: "AIzaSyDXG60896YH8pjO-svO4f7zQlxWBlZHp98",
    }).then((google) => {
      this.google = googleMapApi;
      this.initMap();
    });
  },
};
</script>

<style scoped>
@import "../assets/css/popups.css";
@import "../assets/css/chartstyle.css";
@import "../assets/css/btnstyle.css";
@import "../assets/css/tablestyle.css";

#wrapper {
  position: relative;
}

#container-box {
  position: absolute;
  top: 50px;
  left: 30px;
  z-index: 99;
}

#side-button {
  position: fixed;
  top: 150px;
  left: 300px;
  background-color: black;
}

#sidebarpic {
  position: relative;
  width: 250px;
  height: 180px;

  margin-top: 10px;
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

.tempbar {
  position: absolute;
  bottom: 250px;
  right: 800px;
  z-index: 99;
}

#progress-bar-container {
  width: 400px;
  height: 20px;
  margin: 0 auto;
  position: relative;
  transform: translateY(-50%);
  border-radius: 35px;
  overflow: hidden;
  bottom: 100px;
  right: -685px;
}

.progress-bar-child {
  width: 100%;
  height: 100%;
}

.progress {
  color: white;
  text-align: center;
  line-height: 75px;
  font-size: 35px;
  font-family: "Segoe UI";
  animation-direction: reverse;
  background: #e5405e;

  /* Chrome10-25,Safari5.1-6 */
  background: linear-gradient(to right, #3fffa2 0%, #ffdb3a 45%, #e5405e 100%);
}

.shrinker {
  background-color: gray;
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
}

.timelapse {
  animation-name: timelapse;
  animation-fill-mode: forwards;
  animation-duration: 2s;
  animation-timing-function: cubic-bezier(0.86, 0.05, 0.4, 0.96);
}

#displayBar {
  position: absolute;
  width:300px;
  height:60px;
  bottom: 400px;
  right: 200px;
  z-index: 99;
}

@keyframes timelapse {
  0% {
    width: 100%;
  }
  100% {
    width: 0%;
  }
}

#text1 {
  position: absolute;
  bottom: 110px;
  left: 700px;
}

#text2 {
  position: absolute;
  bottom: 110px;
  left: 850px;
}

#text3 {
  position: absolute;
  bottom: 110px;
  left: 1000px;
}

#text4 {
  position: absolute;
  bottom: 70px;
  left: 700px;
}

#text5 {
  position: absolute;
  bottom: 70px;
  left: 860px;
}

#text6 {
  position: absolute;
  bottom: 70px;
  left: 1000px;
}
</style>
