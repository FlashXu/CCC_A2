<template>

<div id="app">

<div class="search">
      <input type="text" id="input" class="searchTerm" placeholder="Please input SA3 code.">
      <button type="submit" class="searchButton" @click="search">
        <i class="fa fa-search">Search</i>
     </button>
</div>

<button class="linechartBtn" v-on:click="goLine">
          <a id='premium'>Line</a>
</button>
<button class="piechartBtn" v-on:click="goPie">
          <a id='premium'>Pie</a>
</button>
<button class="barchartBtn" v-on:click="goBar">
          <a id='premium'>Bar</a>
</button>
<button class="radarchartBtn" v-on:click="goRadar">
          <a id='premium'>Radar</a>
</button>

<button class="popup" v-on:click="showpopup">Popup
  <div v-if="data.type!='null'" class="popuptext" id="myPopup">
    <piechart :datapath = "data.piedata" :sa3code = "data.sa3code"/> 
    <table id="PopupTable">
      <tr>
        <th>Income(AUD$)</th>
        <th>Num of Twitters</th>
      </tr>
      <tr>
        <td>{{data.income}}</td>
        <td></td>
      </tr>
  </table>
  </div>
</button>

<linechart class="linechart" v-if="data.type=='Line'" :datapath = "data.linedata" :sa3code = "data.sa3code"/>
<piechart class="piechart" v-if="data.type=='Pie'" :datapath = "data.linedata" :sa3code = "data.sa3code"/> 
<barchart class="barchart" v-if="data.type=='Bar'" :datapath = "data.bardata" :sa3code = "data.sa3code"/>
<radarchart class="radarchart" v-if="data.type=='Radar'" :datapath = "data.bardata" :sa3code = "data.sa3code"/>

</div>

</template>

<script>
import datafile from '@/data/AURIN_data.json';
import linechart from '@/charttype/Linechart.vue';
import piechart from '@/charttype/Piechart.vue';
import barchart from '@/charttype/Barchart.vue';
import radarchart from '@/charttype/Radarchart.vue';

export default {
  data(){
    return {
      data:{
        type:"null",
        linedata: datafile,
        piedata: datafile,
        bardata: datafile,
        radardata: datafile,
        sa3code: "null",
        income: "null"
      }
    }

  },
  components:{
    linechart,
    piechart,
    barchart,
    radarchart
  },
  methods:{
    goPie(){
      this.$router.push("piechart");
      var searchbox = document.getElementById("input");
      this.data.sa3code = searchbox.value.toString();
      this.data.type="Pie"; 
      
    },
    goLine(){
      this.$router.push("linechart");
      var searchbox = document.getElementById("input");
      this.data.sa3code = searchbox.value.toString();
      this.data.type="Line";
    },
    goBar(){
      this.$router.push("barchart");
      var searchbox = document.getElementById("input");
      this.data.sa3code = searchbox.value.toString();
      this.data.type="Bar";  
    },
    goRadar(){
      this.$router.push("radarchart");
      var searchbox = document.getElementById("input");
      this.data.sa3code = searchbox.value.toString();
      this.data.type="Radar";  
    },
    showpopup(){
      var popup = document.getElementById("myPopup");
      popup.classList.toggle("show"); 
      var searchbox = document.getElementById("input");
      this.data.sa3code = searchbox.value.toString();
      this.data.income = datafile[this.data.sa3code].income;
    },
    search() {
      var type = this.data.type;
      this.data.type = "null";

      this.$nextTick(() => {
                var searchbox = document.getElementById("input");
                this.data.sa3code = searchbox.value.toString();
                switch(type){
                  case "Pie":
                  case "null":
                    this.data.type = "Pie";
                    break;
                  case "Line":
                    this.data.type = "Line";
                    break;
                  case "Bar":
                    this.data.type = "Bar";
                    break;
                  case "Radar":
                    this.data.type = "Radar";
                    break;
                }
            })
    }
  }
};
</script>

<style>
@import url("./assets/css/popups.css");
@import url("./assets/css/chartstyle.css");
@import url("./assets/css/btnstyle.css");
@import url("./assets/css/tablestyle.css");
</style>