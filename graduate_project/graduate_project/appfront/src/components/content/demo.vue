<template>
  <div v-scroll-spy="{data: 'section'}" style="margin:0px;padding:0px">
    <div style="height:100px;">
         <el-radio-group @change="get_demo_network()" v-model="select_demo" style="margin-left:40%;margin-top:30px;">
          <el-radio-button label="demo1"></el-radio-button>
          <el-radio-button label="demo2"></el-radio-button>
          <el-radio-button label="demo3"></el-radio-button>
         </el-radio-group>
    </div>
    <div >
      <!--<div style="background: rgba(71,88,113,0.9);">-->
        <!--<p style="font-family: Comic Sans MS; font-size:30px; color: #FFFFFF">-->
          <!--Evaluation:-->
        <!--</p>-->
      <!--</div>-->
    <div>
      <el-container style="margin-left:1%; margin-right:1%">
        <div style="border:1px solid #FFFFFF; width:50%">
          <el-row style="background: rgba(71,88,113,0.9); text-align:center; ">
            <span class="demonstration" style="font-size:30px; font-family: Comic Sans MS; color: #FFFFFF; font-style:italic">{{ f_network.type }}</span>
          </el-row>
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Nodes: {{ f_network.nodes_num }}
          </p>
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Edges: {{ f_network.edges_num }}
          </p>
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Average Degree: {{ f_network.aver_degree }}
          </p>
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Known anchor nodes: {{ anchor_known_number }}
          </p>
          <!--<p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">-->
            <!--Real anchor nodes: {{ real_anchor_number }}-->
          <!--</p>-->
        </div>
        <div style="border:1px solid #FFFFFF; width:50%;">
          <el-row style="background: rgba(71,88,113,0.9); text-align:center; ">
            <span class="demonstration" style="font-size:30px; font-family: Comic Sans MS; color: #FFFFFF; font-style:italic">{{ t_network.type }}</span>
          </el-row>
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Nodes: {{ t_network.nodes_num }}
          </p>
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Edges: {{ t_network.edges_num }}
          </p>
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Average Degree: {{ t_network.aver_degree }}
          </p>
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Known anchor nodes: {{ anchor_known_number }}
          </p>
          <!--<p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">-->
            <!--Real anchor nodes: {{ real_anchor_number }}-->
          <!--</p>-->
        </div>
     </el-container>
      <div style="margin-left: 30%;border:1px solid #FFFFFF; width:50%;">
          <el-row style="background-color: #00C5CD; text-align:center; ">
            <span class="demonstration" style="font-size:30px; font-family: Comic Sans MS; color: #FFFFFF; font-style:italic">Aligned Result</span>
          </el-row>
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Alorithm: ISS with η = 4
          </p>
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Predicted anchor user: 137
          </p>
      </div>
      <div style="margin-top:3%; text-align:center; background: rgba(71,88,113,0.9);border-radius:25px;">
        <p style="font-family: Comic Sans MS; font-style:italic; font-size:40px; color: #FFFFFF">
          Evaluation
        </p>
      </div>
      <el-container style="height:300px; background: rgba(71,88,113,0.5);">
      <schart style="margin-left: 20%; width:30%" :canvasId="canvasId1" :height="600" :type="type" :data="ac_data" :options="ac_options"></schart>
      <schart style="margin-left: 10%; width:30%" :canvasId="canvasId2" :height="600" :type="type" :data="f1_data" :options="f1_options"></schart>
      </el-container>
    </div>
   </div>
    <div  class="wrapper" style="margin-top:5%; background: rgba(71,88,113,0.5)">
      <div style="background: rgba(71,88,113,0.9)">
        <el-container>
          <p style="margin-left:30%;font-family: Comic Sans MS; font-size:40px; font-style:italic; color: #ffffff">
            Network View(Only anchor user)
          </p>
          <el-button @click="change_show()" style="margin-left: 10%" icon="el-icon-search"></el-button>
        </el-container>
      </div>
      <el-container v-if="view_show === true" style="opacity:1; margin-right: 1%; margin-left: 1%">
            <network
            class="network"
            ref="f_network"
            :nodes="f_network.nodes"
            :edges="f_network.edges"
            :options="f_network.options" v-loading="loading"
            element-loading-text="while loading"
            element-loading-spinner="el-icon-loading"
            element-loading-background="rgba(0, 0, 0, 0.5)">
            </network>
     </el-container>
    </div>
   <div class="sidebar" style="margin: 0px; border:2px solid #5882bb;">
    <ul class="menu" v-scroll-spy-active="{selector: 'li.menu-item', class: 'customActive'}" v-scroll-spy-link>
        <li class="menu-item">
            <a style="font-family: Comic Sans MS;font-size:20px;">Demo Information</a>
        </li>
        <li class="menu-item">
            <a style="font-family: Comic Sans MS;font-size:20px;">Demo Evaluation</a>
        </li>
        <li class="menu-item">
            <a style="font-family: Comic Sans MS;font-size:20px;">Network View</a>
        </li>
    </ul>
  </div>
</div>
</template>
<script>
import { Timeline, Graph2d, Network } from 'vue2vis';
import Vue from 'vue'
import Schart from 'vue-schart';
import scrollSpy, { Easing } from 'vue2-scrollspy'
Vue.use(scrollSpy, {easing: Easing.Cubic.In})

export default {
  name: 'demo',
  data () {
    return {
      view_show: true,
      canvasId1: 'myCanvas1',
      canvasId2: 'myCanvas2',
      type: 'bar',
      ac_data: [
        {name: 'MNA', value: 0},
        {name: 'MNApna', value: 0},
        {name: 'ISS', value: 0},
      ],
      ac_options: {
        title: 'Accuracy',
        yEqual: 0.5,
      },
      f1_data: [
        {name: 'MNA', value: 0},
        {name: 'MNApna', value: 0},
        {name: 'ISS', value: 0},
      ],
      f1_options: {
        title: 'F1',
        yEqual: 0.5,
      },
      select_demo: 'demo1',
      loading: true,
      run_param:[
        { value: 2, label: "Customize"},
        { value: 1, label: "ISS"},
      ],
      select_run: 1,
      matching:[
        { value: 1, label: "Traditional Stable Matching"},
        { value: 2, label: "Generic Stable Matching"},
        { value: 3, label: "Strict Stable Matching"}
      ],
      select_matching: 1,
      classifier:[
        { value: 1, label: "RandomForest"},
        { value: 2, label: "SVM"},
        { value: 3, label: "AdaBoosting"}
      ],
      select_classifier: 1,
      demo_algorithm: null,
      task_id: null,
      evaluation: null,
      anchor_known_number: 0,
      real_anchor_number: 0,
      labelPosition: 'right',
      formLabelAlign: {
        name: '',
        region: '',
        type: ''
      },
      input: '',
      f_network: {
        type: "foursquare",
        nodes_num: 0,
        edges_num: 0,
        aver_degree: 0,
        nodes: [
        ],
        edges: [
        ],
        anchor_known_list: [
        ],
        options: {
          tooltip: {
            delay: 50,
            fontColor: "black",
            fontSize: 14,
            fontFace: "verdana",
            color: {
              border: "#666",
              background: "#FFFFC6"
              }
          },
          clustering: {
            enabled: false,
            clusterEdgeThreshold: 50
          },
          physics:{
            barnesHut:{
              gravitationalConstant: -60000,
              springConstant:0.02
            }
          },
          nodes: {
            shape: 'dot',
            size: 50,
            font: {
              size: 32,
              color: '#ffffff'
            }
          },
          layout: {improvedLayout:false},
          smoothCurves: {dynamic:false},
          hideEdgesOnDrag: true,
          stabilize: true,
          stabilizationIterations: 10,
          zoomExtentOnStabilize: true,
          navigation: true,
          keyboard: true,
          edges: {
            inheritColor: "to"
          }
        }
      },
      t_network: {
        type: "twitter",
        nodes_num: 0,
        edges_num: 0,
        aver_degree: 0,
        nodes: [],
        edges: [],
        anchor_known_list: [],
        options: {
          physics: {
            maxVelocity: 5,
            minVelocity: 5,
            stabilization: {
              enabled: true,
              iterations: 100,
              updateInterval: 100,
              onlyDynamicEdges: true,
              fit: true
            },
          },
          layout: {
            improvedLayout: false,
          },
          autoResize: true,
          nodes: {
            shape: 'dot',
            size: 30,
            font: {
              size: 32,
              color: '#ffffff'
            },
            borderWidth: 2,
          },
          edges: {
            width: 2
          },
          interaction: {
            hideEdgesOnDrag: true,
            tooltipDelay: 200
          },
        }
      }
    }
  },
  components: {
    Timeline,
    Graph2d,
    Network,
    Schart,
  },
  mounted: function() {
    this.get_demo_network()
  },
  methods: {
    change_show(){
      this.view_show = !this.view_show
    },
    get_demo_network(){
      this.loading = true
      this.$http.get('http://127.0.0.1:8000/api/get_demo_network?demo_name=' + this.select_demo)
        .then((response) => {
            this.loading = true
            var res = JSON.parse(response.bodyText)
            this.f_network.nodes = res.foursquare.nodes.info
            this.f_network.edges = res.foursquare.edges.info
            this.f_network.nodes_num = res.foursquare.nodes.num
            this.f_network.edges_num = res.foursquare.edges.num
            this.t_network.nodes = res.twitter.nodes.info
            this.t_network.edges = res.twitter.edges.info
            this.t_network.nodes_num = res.twitter.nodes.num
            this.t_network.edges_num = res.twitter.edges.num
            this.anchor_known_number = res.anchor_known_num
            this.real_anchor_number = res.real_anchor_num
            this.evaluation = res.evaluation
            this.f_network.aver_degree = res.foursquare.degree
            this.t_network.aver_degree = res.twitter.degree
            this.$set(this.f1_data, 0, {"name":"MNA", "value":this.evaluation["MNA"][0]})
            this.$set(this.f1_data, 1, {"name":"MNApna", "value":this.evaluation["MNApna"][0]})
            this.$set(this.f1_data, 2, {"name":"ISS", "value":this.evaluation["ISS"][0]})
            this.$set(this.ac_data, 0, {"name":"MNA", "value":this.evaluation["MNA"][1]})
            this.$set(this.ac_data, 1, {"name":"MNApna", "value":this.evaluation["MNApna"][1]})
            this.$set(this.ac_data, 2, {"name":"ISS", "value":this.evaluation["ISS"][1]})
            // this.f1_data[1]["value"] = list(this.evaluation["MNApna"])[0]
            // this.f1_data[2]["value"] = list(this.evaluation["ISS"])[0]
            // this.f1_data = res.f1_data
            // this.ac_data = res.ac_data
            this.predicted_num = res.predicted_num
            this.loading = false
        })
    }
  }
}
</script>

<style>
@import 'vue2vis/dist/vue2vis.css';
* {
  font-family: sans-serif;
}
.wrapper {
  position: relative;
  overflow: hidden;
  touch-action: pan-y;
  user-select: none;
  -webkit-user-drag: none;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  width: 100%;
  height: 100%;
}
.events {
  text-align: left;
  height: 70px;
}
.network {
  height: 700px;
  width: 70%;
  margin-left: 15%;
  border: 1px solid #ccc;
  font-color: #FFFFFF;
}
.p {
  font-family: Comic Sans MS;
  font-size:20px;
}
.sidebar {
        position: fixed;
        top: 300px;
        right: 0px;
        max-width: 230px;
        font-size: 15px;
        color: #FFFFFF;
        background: rgba(71,88,113,0.8);
}
.a{
  font-family: Comic Sans MS;
  font-size:17px;
}
.menu {
        padding: 0;
        list-style: none;
        margin: 0px;
}
.customActive {
        background-color: #00C5CD;
        transition: all 0.5s;
    }
.menu-item {
        margin-bottom: 20px;
    }
    .menu-item a {
        cursor: pointer;
    }
</style>
