<script>
import { Line } from 'vue-chartjs'
export default {
  props:["datapath"],
  extends: Line,
  data() {
    return{
      linedata: this.datapath.line.data,
      option:this.datapath.bar.options
    }
  },
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart(this.linedata, this.option)
  }
}


</script>
