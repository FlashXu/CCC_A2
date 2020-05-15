<script>
import { Line } from 'vue-chartjs'
export default {
  props:["datapath", "sa3code"],
  extends: Line,
  data() {
    return{
    }
  },
  mounted () {
    var strs = new Array(); 
    strs = this.sa3code.split(","); 
    
    var input_dataset = [];
    var instance = {};
    var bgColor = ["#ff6384","#36a2eb", "#ffcd56", "#60ffb7", "#e34722", "#3069cd",
                    "#e253ea", "#bde944", "#1da375", "#ae7006"];

    for (var i = 0; i < strs.length; i++) { 
    instance = {};
    instance['backgroundColor'] = bgColor[i];
    instance['borderColor'] = bgColor[i];
    instance['pointHoverBackgroundColor'] = bgColor[i];
    instance['pointHoverBorderColor'] = "rgb(255,255,255)";
    instance['pointBackgroundColor'] = bgColor[i];
    instance['pointBorderColor'] ="rgb(255,255,255)";
    instance['data'] = [this.datapath[strs[i]].teen_num, 
            this.datapath[strs[i]].middle_num, this.datapath[strs[i]].old_num];
    
    instance['label'] = this.datapath[strs[i]].sa3name;
    instance['fill'] = false;
    input_dataset[i] = instance;   
 }


    var linedata = {
      labels: ["Number of Teenagers", "Number of Middle-aged", "Number of The Old"],
      datasets: input_dataset
    }
    var options = {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }    
          }]
        },
        plugins:{
         datalabels: {
           display: false,
          
        }
     }
        
        
      }
    // Overwriting base render method with actual data.
    this.renderChart(linedata, options)
  }
}


</script>
