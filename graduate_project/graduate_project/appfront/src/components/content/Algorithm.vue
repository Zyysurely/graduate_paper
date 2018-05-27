<template>
<div v-scroll-spy="{data: 'section'}" style="margin:0px;padding:0px">
  <div>
     <div style="height:50px; background: rgba(71,88,113,0.9)">
       <p style="font-family: Comic Sans MS; font-size:30px; color: #00C5CD">
          Hi, {{ user_name }}
        </p>
      </div>
      <div style="background: rgba(71,88,113,0.9)">
        <p style="font-family: Comic Sans MS; font-size:30px; color: #ffffff">
          You can choose the param to set your algorithm and see the real-word social network datasets below.
        </p>
      </div>
    <div style="border:1px solid #FFFFFF; margin-right:1%; margin-left:1%; margin-top:2%; margin-bottom:2%">
      <el-row style="background: rgba(71,88,113,0.9); text-align:center; ">
        <span class="demonstration" style="font-family: Comic Sans MS; font-size:25px; color: #FFFFFF; font-style:italic">Algorithm Setting</span>
      </el-row>
      <el-container style="margin-left:10%; margin-top:10px; margin-bottom:20px">
        <span class="demonstration" style="font-family: Comic Sans MS; font-size:25px; color: #00C5CD">Algorithm:</span>
        <el-tooltip class="item" effect="dark" content="you can choose classifier here" placement="top">
          <el-select v-model="select_run" placeholder="算法选择">
            <el-option
              v-for="item in run_param"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-tooltip>
        <span v-if="select_run === 1" class="demonstration" style="margin-left:2%; font-family: Comic Sans MS; font-size:25px; color: #00C5CD">Iterations:</span>
        <el-tooltip v-if="select_run === 1" class="item" effect="dark" content="you can choose classifier here" placement="top">
           <el-input-number v-model="ISS_k" size="medium"></el-input-number>
        </el-tooltip>
        <span v-if="select_run === 2" class="demonstration" style="margin-left:2%;font-family: Comic Sans MS; font-size:25px; color: #00C5CD">Classifier:</span>
        <el-tooltip v-if="select_run === 2" class="item" effect="dark" content="you can choose classifier here" placement="top">
          <el-select v-model="select_classifier" placeholder="分类器">
            <el-option
              v-for="item in classifier"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-tooltip>
        <span v-if="select_run === 2" class="demonstration" style="margin-left:2%;font-family: Comic Sans MS; font-size:25px; color: #00C5CD">Matching:</span>
        <el-tooltip v-if="select_run === 2" class="item" effect="dark" content="you can choose classifier here" placement="top">
          <el-select v-model="select_matching" placeholder="配对">
            <el-option
              v-for="item in matching"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-tooltip>
        <span v-if="select_matching === 2&&select_run === 2" class="demonstration" style="margin-left:2%;font-family: Comic Sans MS; font-size:25px; color: #00C5CD">K:</span>
        <el-tooltip v-if="select_matching === 2&&select_run === 2" class="item" effect="dark" content="k of Generic stable matching setting" placement="top">
           <el-input-number v-model="matching_k" size="medium"></el-input-number>
        </el-tooltip>
        <el-button style="margin-left:5%;"@click="run_al()">Start</el-button>
      </el-container>
     </div>
  </div>
   <div class="wrapper" style="background: rgba(71,88,113,0.5)">
    <el-container style="margin-top: 10px; margin-bottom: 10px">
       <span class="demonstration" style="margin-left:25%; font-family: Comic Sans MS; font-size:20px; color: #00C5CD">Anchor Known Nodes</span>
       <el-input-number :max="real_anchor_number" v-model="anchor_known_number" size="medium"></el-input-number>
      <span class="demonstration" style="margin-left:5%; font-family: Comic Sans MS; font-size:20px; color: #00C5CD">Degree Limit</span>
      <el-input-number v-model="degree" size="medium"></el-input-number>
       <el-button style="margin-left: 3%" @click="fresh_network()">Set</el-button>
    </el-container>
    <!--<el-container style="opacity:1;margin-left:20px;margin-top:30px">-->
      <!--<span class="demonstration" style="font-family: Comic Sans MS; font-size:20px; color: #00C5CD">Nodes</span>-->
      <!--<el-slider :min="0" :max="init_tw_nodes" show-input v-model="f_network.nodes_num" style="margin-left: 10px; width: 35%"></el-slider>-->
      <!--<span class="demonstration" style="margin-left: 200px; font-family: Comic Sans MS; font-size:20px; color: #00C5CD">Nodes</span>-->
      <!--<el-slider :min="0" :max="init_four_nodes" show-input v-model="t_network.nodes_num" style="margin-left: 10px; width: 35%"></el-slider>-->
     <!--</el-container>-->
     <el-container style="margin-left:1%; margin-right:1%">
        <div style="border:1px solid #FFFFFF; width:50%">
          <div style="background: rgba(71,88,113,0.9);">
            <el-select v-model="f_network.type" placeholder="请选择" @change="dul_dataset()">
              <el-option
                v-for="item in all_dataset"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </div>
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
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Real anchor nodes: {{ real_anchor_number }}
          </p>
        </div>
        <div style="border:1px solid #FFFFFF; width:50%;">
          <div style="background: rgba(71,88,113,0.9);">
              <el-select style="margin-left:0px" v-model="t_network.type" @change="dul_dataset()" placeholder="请选择">
                <el-option
                  v-for="item in all_dataset"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </div>
          <el-row style="background: rgba(71,88,113,0.9);text-align:center; ">
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
          <p style="font-family: Comic Sans MS; font-size:20px; color: #ffffff; text-align:center">
            Real anchor nodes: {{ real_anchor_number }}
          </p>
        </div>
     </el-container>
  </div>
  <div class="wrapper" style="background: rgba(71,88,113,0.4); margin:0px;padding:0px">
    <el-container style="opacity:1; margin-right: 1%; margin-left: 1%">
          <network
          class="network"
          ref="f_network"
          :nodes="f_network.nodes"
          :edges="f_network.edges"
          :options="f_network.options" v-loading="loading"
          element-loading-text="while loading"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.5)"
          style="height: 700px;
  width: 50%;
  border: 1px solid #ccc;
  margin: 5px 0;
  font-color: #FFFFFF;">
          </network>
          <network
          class="network"
          ref="t_network"
          :nodes="t_network.nodes"
          :edges="t_network.edges"
          :options="t_network.options" v-loading="loading"
          element-loading-text="while loading"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.5)"
          style="height: 700px;
  width: 50%;
  border: 1px solid #ccc;
  margin: 5px 0;
  font-color: #FFFFFF;">
          </network>
   </el-container>
  </div>
  <div>
  </div>
  <div class="sidebar" style="margin: 0px; border:2px solid #5882bb;">
    <ul class="menu" v-scroll-spy-active="{selector: 'li.menu-item', class: 'customActive'}" v-scroll-spy-link>
        <li class="menu-item">
            <a style="font-family: Comic Sans MS;font-size:20px;">Algorithm setting</a>
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
import scrollSpy, { Easing } from 'vue2-scrollspy'
Vue.use(scrollSpy, {easing: Easing.Cubic.In})

export default {
  name: 'algorithm',
  data () {
    return {
      init_four_nodes: 1000,
      init_tw_nodes: 1000,
      user_name: null,
      ISS_k: 1,
      matching_k: 1,
      loading: true,
      degree: 0,
      all_dataset: [
        { value: "foursquare", label: "foursquare"},
        { value: "twitter", label: "twitter"},
      ],
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
      task_id: null,
      anchor_known_number: 0,
      real_anchor_number: 0,
      f_anchor_known_list: [],
      t_anchor_known_list: [],
      labelPosition: 'right',
      formLabelAlign: {
        name: '',
        region: '',
        type: ''
      },
      input: '',
      f_network: {
        type: "foursquare",
        nodes_num: 50,
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
            size: 60,
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
          borderWidth: 2,
          edges: {
            width: 4,
            inheritColor: "to"
          }
        }
      },
      t_network: {
        type: "twitter",
        nodes_num: 50,
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
            size: 60,
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
          borderWidth: 2,
          edges: {
            width: 4,
            inheritColor: "to"
          }
        }
      }
    }
  },
  components: {
    Timeline,
    Graph2d,
    Network,
  },
  mounted: function() {
      this.init_network()
  },
  methods: {
    init_network(){
      this.loading = true
      this.user_name = sessionStorage.getItem('user_name')
      this.$http.get('http://127.0.0.1:8000/api/init_network')
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.f_network.nodes = res.foursquare.nodes.info
            this.f_network.edges = res.foursquare.edges.info
            this.f_network.anchor_known_list = res.foursquare.anchor_known_list
            this.f_network.nodes_num = res.foursquare.nodes.num
            this.f_network.edges_num = res.foursquare.edges.num
            this.t_network.nodes = res.twitter.nodes.info
            this.t_network.edges = res.twitter.edges.info
            this.t_network.anchor_known_list = res.twitter.anchor_known_list
            this.t_network.nodes_num = res.twitter.nodes.num
            this.t_network.edges_num = res.twitter.edges.num
            this.real_anchor_number = res.real_anchor_num
            this.f_network.aver_degree = res.foursquare.degree
            this.t_network.aver_degree = res.twitter.degree
            this.anchor_known_number = res.anchor_known_num
            this.task_id = 'init'
            this.loading = false
        })
    },
    dul_dataset(){
      if(this.f_network.type == this.t_network.type){
        return this.$confirm("The choosen datasets must be different!!!")
      }
    },
    fresh_network(){
      this.loading = true
      this.$http.post('http://127.0.0.1:8000/api/fresh_network', {
        user_name: this.user_name,
        four_type: this.f_network.type,
        tw_type: this.t_network.type,
        four_num:this.f_network.nodes_num,
        tw_num: this.t_network.nodes_num,
        anchor_known_number: this.anchor_known_number,
        degree: this.degree},
        {emulateJSON: true})
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.f_network.nodes = res.foursquare.nodes.info
            this.f_network.edges = res.foursquare.edges.info
            this.f_network.nodes_num = res.foursquare.nodes.num
            this.f_network.edges_num = res.foursquare.edges.num
            this.t_network.nodes = res.twitter.nodes.info
            this.t_network.edges = res.twitter.edges.info
            this.t_network.nodes_num = res.twitter.nodes.num
            this.t_network.edges_num = res.twitter.edges.num
            this.real_anchor_number = res.real_anchor_num
            this.task_id = res.task_id
            this.loading = false
        })
    },
    run_al(){
      this.$http.post('http://127.0.0.1:8000/api/run_al', {
         task_id: this.task_id,
         algorithm: this.select_run,
         matching: this.select_matching,
         classifier: this.select_classifier,
         iss_k: this.ISS_k,
         matching_k: this.matching_k
         },
         {emulateJSON: true})
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.show = res.success
            const h = this.$createElement
            if (res.success == "yes") {
              this.$notify({
                title: 'running task' + this.task_id,
                message: h('i', { style: 'color: teal'}, 'Your task' + this.task_id + 'starts successfully, you can check the status in result')
              })
            } else {
              this.$notify({
                title: 'running task' + this.task_id,
                message: h('i', { style: 'color: teal'}, 'Your task' + this.task_id + 'starts failed, you can check the status in result')
              })
            }
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
