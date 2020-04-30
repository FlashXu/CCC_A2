<template>
  <div>
    <!-- <div class="page-header clear-filter">
      <div class="page-header-image" style="height:8%;background-color:black"></div>
    </div> -->
    <div id ='gmap' style="width: 100%; height: 1000px;"></div>
  </div>
</template>


<script>
import MainFooter from '@/layout/MainFooter';
import GoogleMapsApiLoader from 'google-maps-api-loader'

export default {
  name: 'maps-page',
  bodyClass: 'maps-page',

  methods: {
    initMap() {
      // Styles a map in night mode.
      var map = new google.maps.Map(document.getElementById("gmap"), {
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
      console.log('before load json in VUE');
      map.data.loadGeoJson('./GeoJson-Data-master/australian-states.json');
      console.log('after load json in VUE');
      
      //   map.mapTypes.set('myStyle', myStyle);
      //   map.setMapTypeId('myStyle');
    
      //   map.data.setStyle((feature) => ({
      //     fillColor: "red",s
      //   }));
    
      // auto zoom after click one region
      map.data.addListener("click", function (e) {
        let bounds = new google.maps.LatLngBounds();
    
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
  },
  mounted() {
    const googleMapApi = GoogleMapsApiLoader({
      apiKey: 'AIzaSyDXG60896YH8pjO-svO4f7zQlxWBlZHp98',
    }).then((google)=>{
      this.google = googleMapApi;
      this.initMap();
    })
  }
};
</script>

<style></style>


<!--
<template>
  <div class="page-header clear-filter">
    <div class="page-header-image" style="height:8%;background-color:black"></div>
    <div class="content">
      <div>
        <div>
          <h2>Search and add a pin</h2>
          <label>
            <gmap-autocomplete
              @place_changed="setPlace">
            </gmap-autocomplete>
            <button @click="addMarker">Add</button>
          </label>
          <br/>
        </div>
        <br>
        <gmap-map
          :center="center"
          :zoom="12"
          style="width:100%;  height: 800px;"
        >
          <gmap-marker
            :key="index"
            v-for="(m, index) in markers"
            :position="m.position"
            @click="center=m.position"
          ></gmap-marker>
        </gmap-map>
      </div>
    </div>
  </div>  
</template>

<script>
export default {
  name: "maps-page",
  data() {
    return {
      // default to Montreal to keep it simple
      // change this to whatever makes sense
      center: { lat: 45.508, lng: -73.587 },
      markers: [],
      places: [],
      currentPlace: null
    };
  },

  mounted() {
    this.geolocate();
  },

  methods: {
    // receives a place object via the autocomplete component
    setPlace(place) {
      this.currentPlace = place;
    },
    addMarker() {
      if (this.currentPlace) {
        const marker = {
          lat: this.currentPlace.geometry.location.lat(),
          lng: this.currentPlace.geometry.location.lng()
        };
        this.markers.push({ position: marker });
        this.places.push(this.currentPlace);
        this.center = marker;
        this.currentPlace = null;
      }
    },
    geolocate: function() {
      navigator.geolocation.getCurrentPosition(position => {
        this.center = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
      });
    }
  }
};
</script>

<style></style>
 -->
