<script>
import {Bar} from 'vue-chartjs'
export default {
  props:["datapath", "sa3code", "tweetpath", "mixedtype"],
  extends: Bar,
  data() {
    return{
    }
  },
  mounted () {
    try{
    
    var strs = new Array(); 
    strs = this.sa3code.split(","); 
    for(var i = 0; i<strs.length; i++){
      strs[i] =  strs[i].trim();
    } 
    
    var input_dataset = [];
    var instance = {};
    var bgColor = ["#ff6384","#36a2eb", "#ffcd56", "#60ffb7", "#e34722", "#3069cd",
                    "#e253ea", "#bde944", "#1da375", "#ae7006"];
    var bardatalabel = [];
    var tweetcountlist = [];

    if (this.mixedtype == "Mixed1"){
    

        var youngdata = [];
        var middata =[];
        var olddata = []; 

        for (var j = 0; j < strs.length; j++) {
            
            youngdata.push(this.datapath[strs[j]].teen_num);
            middata.push(this.datapath[strs[j]].middle_num);
            olddata.push(this.datapath[strs[j]].old_num);
            bardatalabel.push(this.datapath[strs[j]].sa3name)
            tweetcountlist.push(this.tweetpath[strs[j]])
        }

        var agedata = [youngdata, middata, olddata]
        var agelabel = ["Number of Teenagers", "Number of Middle-aged", "Number of The Old"];

        for (var i = 0; i < 3; i++) { 
            instance = {};
            instance['backgroundColor'] = bgColor[i];
            instance['data'] = agedata[i];
            instance['label'] = agelabel[i];
            instance['order'] = i+2;
            instance['yAxisID'] = 'A';
            input_dataset.push(instance); 
            
        }
    }else{
        var incomelist = [];
    
        for (var j = 0; j < strs.length; j++) {
            incomelist.push(this.datapath[strs[j]].income);
            bardatalabel.push(this.datapath[strs[j]].sa3name)
            tweetcountlist.push(this.tweetpath[strs[j]])
        }

        instance = {};
        instance['backgroundColor'] = bgColor[1];
        instance['data'] = incomelist;
        instance['label'] = "Mean Anual Income in AUD($)";
        instance['order'] = 2;
        instance['yAxisID'] = 'A';
        input_dataset.push(instance); 
    }

    instance = {};

    instance['backgroundColor'] = "grey";
    instance['borderColor'] = "grey";
    instance['pointHoverBackgroundColor'] = "grey";
    instance['pointHoverBorderColor'] = "rgb(255,255,255)";
    instance['pointBackgroundColor'] = "grey";
    instance['pointBorderColor'] ="rgb(255,255,255)";
    instance['fill'] = false,

    instance['data'] = tweetcountlist;
    instance['label'] = "Number of Tweets";
    instance['type'] = 'line';
    instance['order'] = 1;
    instance['yAxisID'] = 'B';
    input_dataset.push(instance)
 
    var bardata = {
      labels: bardatalabel,
      datasets: input_dataset
    }
    var options = {
        scales: {
          yAxes: [
        {
        id: 'A',
        type: 'linear',
        position: 'left',
        ticks: {
              beginAtZero: true
            }    
      },
      {
        id: 'B',
        type: 'linear',
        position: 'right',
        ticks: {
              beginAtZero: true
            }     
      }
          ]
        },
        plugins:{
         datalabels: {
           display: false     
        }
     }

      }
    // Overwriting base render method with actual data.
    this.renderChart(bardata, options)
    }catch(err){

    }
  }
}
</script>