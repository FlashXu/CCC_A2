<script>
import {Radar} from 'vue-chartjs'
export default {
  props:["datapath", "sa3code"],
  extends: Radar,
  data() {
    return{
    }
  },
  mounted() {
    var strs = new Array(); 
    strs = this.sa3code.split(","); 
    
    var input_dataset = [];
    var instance = {};
    var bdColor = ["#ff6384","#36a2eb", "#ffcd56", "#60ffb7", "#e34722", "#3069cd",
                    "#e253ea", "#bde944", "#1da375", "#ae7006"];

    var bgColor = ["rgba(255,99,132,0.2)","rgba(54,162,235,0.2)", "rgba(255,205,86,0.2)", 
                    "rgba(96,255,183,0.2)", "rgba(227,71,34,0.2)", "rgba(48,105,205,0.2)",
                    "rgba(181,32,145,0.2)", "rgba(189,233,68,0.2)", "rgba(29,163,117,0.2)", "rgba(174,112,6,0.2)"];

    for (var i = 0; i < strs.length; i++) { 
        instance = {};
        instance['backgroundColor'] = bgColor[i];
        instance['borderColor'] = bdColor[i];
        instance['pointHoverBackgroundColor'] = bdColor[i];
        instance['pointHoverBorderColor'] = "rgb(255,255,255)";
        instance['pointBackgroundColor'] = bdColor[i];
        instance['pointBorderColor'] ="rgb(255,255,255)";
        instance['data'] = [this.datapath[strs[i]].teen_num, 
                this.datapath[strs[i]].middle_num, this.datapath[strs[i]].old_num];
        
        instance['label'] = this.datapath[strs[i]].sa3name;
        instance['fill'] = true;
        input_dataset[i] = instance;   
 }
    
    var radardata = {
      labels: ["Number of Teenagers", "Number of Middle-aged", "Number of The Old"],
      datasets: input_dataset
    }
    var options ={}
    // Overwriting base render method with actual data.
    this.renderChart(radardata, options)
  }
}


</script>
