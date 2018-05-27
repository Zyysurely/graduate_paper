<template>
  <div class="wrapper" style="background: rgba(71,88,113,0.5)">
      <p style="font-family: Comic Sans MS; font-size:30px; color: #00C5CD">
          Hi, Administrator {{ username }}
      </p>
      <div style="background: rgba(71,88,113,0.9); border-radius:25px;">
        <p style="text-align: center; font-style:italic; font-family: Comic Sans MS; font-size:40px; color: #ffffff; height:100px;">
          Dataset Management
        </p>
      </div>
      <div style="height:300px; margin-top:1%; background-color: white; margin-left:15%; margin-right:15%; border:2px solid #5882bb;">
      <div>{{ s }} </div>
      <el-upload
        class="upload-demo"
        ref="upload"
        action="http://127.0.0.1:8000/api/upload_dataset"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :file-list="fileList"
        :before-remove="beforeRemove"
        :auto-upload="false"
        :on-success="handleUpload">
       <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
        <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
        <div slot="tip" class="el-upload_tip">只能上传gpickle格式文件，且不超过500kb</div>
      </el-upload>
    </div>
    <div style="margin-top: 9%; background: rgba(71,88,113,0.9); border-radius:25px;">
        <p style="text-align: center; font-style:italic; font-family: Comic Sans MS; font-size:40px; color: #ffffff; height:100px;">
          User Management
        </p>
    </div>
    <div style="margin-top:1%; margin-left:10%; margin-right:10%">
          <el-table
              :data="userList"
              max-height="500"
              style="width: 100%">
              <el-table-column
                  prop="username"
                  label="Username">
                </el-table-column>
                <el-table-column
                  prop="authority"
                  label="Authority"
                  width="180" style="background: rgba(71,88,113,0.5)">
                </el-table-column>
                <el-table-column label="Manage">
                  <template slot-scope="scope">
                    <el-button
                      type="primary"
                      v-if="scope.row.authority === 'True'&&scope.row.username!=username" @click="get_task_network(scope.$index, scope.row)">downgrade</el-button>
                    <el-button
                      type="primary"
                      v-if="scope.row.authority === 'False'&&scope.row.username!=username" @click="handleDelete(scope.$index, scope.row)">upgrade</el-button>
                    <el-button
                      type="danger"
                      v-if="scope.row.username!=username"
                      @click="handleDelete(scope.$index, scope.row)">delete</el-button>
                  </template>
                </el-table-column>
          </el-table>
      </div>
  </div>
</template>
<script>
export default {
  name: 'dataManagement',
  data() {
      return {
        fileList: [],
        userList: [],
        username: [],
        s: null,
      };
  },
  mounted: function() {
    this.username = sessionStorage.getItem('user_name');
    this.get_dataset_list();
    this.get_user_list()
  },
  methods: {
    submitUpload() {
        this.$refs.upload.submit();
    },
    handleUpload(response, file, fileList) {
        this.s = response
        this.$http.post('http://127.0.0.1:8000/api/operate_dataset', {
           operation: 2,
           name: file.id,
           url: file.url
         },
         {emulateJSON: true})
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            const h = this.$createElement
            if (res.success == "yes") {
              this.$notify({
                title: 'Uploaded Successfully',
              })
            } else {
              this.$notify({
                title: 'Uploaded Failed',
              })
            }
        })
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
      this.s = file
      this.$http.post('http://127.0.0.1:8000/api/operate_dataset', {
           operation: 1,
           name: file.id,
           url: file.url
         },
         {emulateJSON: true})
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            const h = this.$createElement
            if (res.success == "yes") {
              this.$notify({
                title: 'Uploaded Successfully',
              })
            } else {
              this.$notify({
                title: 'Uploaded Failed',
              })
            }
        })
    },
    handlePreview(file) {
      console.log(file);
    },
    get_dataset_list() {
      this.$http.get('http://127.0.0.1:8000/api/get_dataset_list')
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.fileList = res.datasetlist
        })
    },
    get_user_list() {
      this.$http.get('http://127.0.0.1:8000/api/get_user_list')
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.userList = res.user_list
        })
    },
    beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
    }
  }
}
</script>

<style rel="stylesheet/scss"lang="scss">
.el-upload_tip {
  font-size: 30px;
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
</style>
