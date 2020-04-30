<script>
import {Pie} from 'vue-chartjs'
export default {
  props:["datapath"],
  extends: Pie,
  data() {
    return{
      piedata: this.datapath.pie.data,
      option:this.datapath.pie.options
    }
  },
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart(this.piedata, this.option)
  }
}


</script>
