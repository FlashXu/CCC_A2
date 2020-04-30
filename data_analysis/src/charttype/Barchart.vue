<script>
import {Bar} from 'vue-chartjs'
export default {
  props:["datapath"],
  extends: Bar,
  data() {
    return{
      bardata: this.datapath.bar.data,
      option:this.datapath.bar.options
    }
  },
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart(this.bardata, this.option)
  }
}
</script>