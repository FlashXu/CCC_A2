<template>

<div id="app">
<button class="linechart" v-on:click="goLine">
          <a id='premium'>Linechart</a>
</button>
<button class="piechart" v-on:click="goPie">
          <a id='premium'>Piedata</a>
</button>
<button class="barchart" v-on:click="goBar">
          <a id='premium'>Barchart</a>
</button>

<linechart v-if="data.type=='Line'" :datapath = "data.linedata"/>
<piechart v-if="data.type=='Pie'" :datapath = "data.piedata"/> 
<barchart v-if="data.type=='Bar'" :datapath = "data.bardata"/>


</div>

</template>

<script>
import datafile from '@/data/data.json';
import linechart from '@/charttype/Linechart.vue';
import piechart from '@/charttype/Piechart.vue';
import barchart from '@/charttype/Barchart.vue';

export default {
  data(){
    return {
      data:{
        type:"null",
        linedata: datafile,
        piedata: datafile,
        bardata: datafile
      }
    }

  },
  components:{
    linechart,
    piechart,
    barchart
  },
  methods:{
    goPie(){
      // window.location.href="/piechart";
      this.$router.push("piechart");
      this.data.type="Pie"; 


   
    },
    goLine(){
      // window.location.href="/linechart";
      this.$router.push("linechart");
      this.data.type="Line";

      
    },
    goBar(){
      // window.location.href="/barchart";
      this.$router.push("barchart");
      this.data.type="Bar";  
      
    }

  }
};
</script>

<style>
</style>