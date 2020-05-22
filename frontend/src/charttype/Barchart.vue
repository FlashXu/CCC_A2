<script>
import {Bar} from 'vue-chartjs'
export default {
  props:["datapath", "sa3code"],
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

    if(this.datapath.hasOwnProperty("twtnum")){
      
    function f(a,b) {  
        return b-a; 
      }
    var lang = this.datapath['lang'];
    var lang_list = [];
    var lang_freq = [];
    var old_freq = [];
    for(var key in lang){
        if(key == 'en')continue;
        lang_list.push(key)
        lang_freq.push(lang[key])
        old_freq.push(lang[key])
      }
  
    lang_freq.sort(f);
    var tweet_labels = [];
    var tweet_freq = [];

    instance['backgroundColor'] = [];
    var count = 0;
    var former_freq = 0;
    var currentmax = 0;

    for (var i = 0; i < lang_freq.length; i++){
    currentmax = lang_freq[i]
    if (currentmax == former_freq){
      continue;
    }
    for (var j = 0; j < old_freq.length; j++){
      if (old_freq[j] == currentmax){
        instance['backgroundColor'].push(bgColor[count])
        count++;
        tweet_labels.push(lang_list[j]);
        tweet_freq.push(currentmax);    
      }
      if (count>5){break;}
    }
    if (count>5){break;}
    former_freq = currentmax;
  }
  instance['data'] = tweet_freq;
  instance['label'] = this.sa3code;
  input_dataset[0] = instance;
  var bardata = {
      labels: tweet_labels,
      datasets: input_dataset
    }
    var options = {
      legend: {
             display: false,
              },
        scales: {
          yAxes: [{
            gridLines: {
              
              color: "#fff",
              
            },
            ticks: {
              beginAtZero: true,
              fontColor:'white'
            }    
          }],
          xAxes: [{
            gridLines: {
              
              color: "#fff",
              
            },
            ticks: {
              fontColor:'white'
              
            }    
          }]
        },
        plugins:{
         datalabels: {
           display: true,
           color: '#fff'
          
        }
     }

      }
    // Overwriting base render method with actual data.
    this.renderChart(bardata, options)
  

    }else{

    for (var i = 0; i < strs.length; i++) { 
    instance = {};
    instance['backgroundColor'] = bgColor[i];
    instance['data'] = [this.datapath[strs[i]].teen_num, 
            this.datapath[strs[i]].middle_num, this.datapath[strs[i]].old_num];
    
    instance['label'] = this.datapath[strs[i]].sa3name;
    input_dataset[i] = instance;   
 }
 
    var bardata = {
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
           display: true,
           color: '#fff'
          
        }
     }

      }
    // Overwriting base render method with actual data.
    this.renderChart(bardata, options)
  }
 
    
  }catch(err){

  }
}
}
</script>