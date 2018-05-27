<template>
  <div v-scroll-spy="{data: 'section'}" style="margin:0px;padding:0px">
    <div class="wrapper" style="background: rgba(71,88,113,0.5)">
      <div style="margin-left:10%; margin-right:10%">
          <el-table
              :data="task_list"
              max-height="500"
              style="width: 100%">
              <el-table-column type="expand">
                <template slot-scope="props">
                  <el-form v-for="(value, key) in props.row.algorithm" label-position="left" inline class="demo-table-expand">
                    <el-form-item>
                      <span>{{ key }}:</span>
                      <span>{{ value }}</span>
                    </el-form-item>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column
                  prop="task_id"
                  label="task_id">
                </el-table-column>
                <el-table-column
                  prop="start_time"
                  label="Start_time"
                  width="180" style="background: rgba(71,88,113,0.5)">
                </el-table-column>
                <el-table-column
                  prop="end_time"
                  label="End_time"
                  width="180">
                </el-table-column>
                <el-table-column
                  prop="already"
                  label="Already"
                  width="180">
                </el-table-column>
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button
                      type="primary"
                      @click="get_task_network(scope.$index, scope.row)">Show View</el-button>
                    <el-button
                      type="danger"
                      @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
                  </template>
                </el-table-column>
          </el-table>
      </div>
     <div class="wrapper" style="background: rgba(71,88,113,0.5)" v-if="select_task.length">
       <span class="demonstration" style="font-size:30px; font-family: Comic Sans MS; color: #FFFFFF; font-style:italic">Task:{{ select_task }}</span>
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
            Real anchor nodes: {{ real_anchor_number }}
          </p>
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
            Known anchor nodes: {{ t_network.anchor_known_list.length }}
          </p>
        </div>
     </el-container>
  </div>
  <div class="wrapper" style="margin-top:30px; background: rgba(71,88,113,0.4); margin:0px;padding:0px">
    <el-container style=" opacity:1; margin-right: 1%; margin-left: 1%" v-if="before_show === 1">
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
  name: 'result',
  data () {
    return {
      visible2: false,
      loading: true,
      user_name: null,
      before_show: 0,
      aligned_show: 0,
      select_task: '',
      task_list: [],
      select_demo: '',
      loading: false,
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
      predicted_anchor_list: [],
      predicted_anchor_number: 0,
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
          physics:{
            maxVelocity: 10,
            minVelocity: 10,
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
          physics:{
            maxVelocity: 10,
            minVelocity: 10,
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
      },
      aligned_network: {
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
          physics:{
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
    this.get_task_list()
  },
  methods: {
    get_task_list(){
      this.user_name = sessionStorage.getItem('user_name');
      this.$http.get('http://127.0.0.1:8000/api/get_task_list?user_name=' + this.user_name)
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.task_list = res.task
      })
    },
    get_task_network(index, row){
      this.select_task = row.task_id
      this.before_show = 1
      this.loading = true
      this.$http.get('http://127.0.0.1:8000/api/get_task_network?task_name=' + this.select_task)
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
            this.f_network.aver_degree = res.foursquare.degree
            this.t_network.aver_degree = res.twitter.degree
            // this.anchor_known_number = res.anchor_known_number
            // this.real_anchor_number = res.real_anchor_num
            this.loading = false
        })
    },
    handleDelete(index, row){
      this.visible2 = false
      this.$confirm(`确定移除 ${ row.task_id }？`)
        .then(_=>{
              this.$http.get('http://127.0.0.1:8000/api/del_task?task_name=' + row.task_id)
                .then((response) => {
                    var res = JSON.parse(response.bodyText)
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
                this.task_list.splice(index, 1);})
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
