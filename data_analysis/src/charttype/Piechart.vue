
<script>
import {Pie} from 'vue-chartjs'
export default {
  props:["datapath", "sa3code"],
  extends: Pie,
  data() {
    return{
    }
  },
  mounted() {
        var strs = new Array(); 
    strs = this.sa3code.split(","); 
    
    var input_dataset = [];
    var instance = {};
    var bgColor = ["#ff6384","#36a2eb", "#ffcd56", "#60ffb7", "#e34722", "#3069cd",
                    "#e253ea", "#bde944", "#1da375", "#ae7006"];

    for (var i = 0; i < strs.length; i++) { 
    instance = {};
    
    
    instance['backgroundColor'] = [bgColor[0], bgColor[1], bgColor[2]];
    instance['data'] = [this.datapath[strs[i]].teen_num, 
            this.datapath[strs[i]].middle_num, this.datapath[strs[i]].old_num];
    
    instance['label'] = this.datapath[strs[i]].sa3name;
    input_dataset[i] = instance;   
 }
    
    var piedata = {
      labels: ["Number of Teenagers", "Number of Middle-aged", "Number of The Old"],
      datasets: input_dataset
    }

    var options ={
       tooltips: {
        custom: function(tooltip) {
          if (!tooltip) return;
          // disable displaying the color box;
          tooltip.displayColors = false;
        },
        callbacks: {
          label: function(tooltipItem, data) {
            var dataset = data.datasets[tooltipItem.datasetIndex];
            var total = 0;
            for(var i = 0; i<dataset.data.length; i++){
              total +=dataset.data[i];
            }
            var percentage = (dataset.data[tooltipItem.index]/total)*100
          
            return [dataset.label, data.labels[tooltipItem.index] + ": " + dataset.data[tooltipItem.index] , ("Percentage: " + percentage.toFixed(2) + "%")];
          }
        }
      }
    };               
 
    // Overwriting base render method with actual data.
    this.renderChart(piedata, options)

  }
}


</script>
