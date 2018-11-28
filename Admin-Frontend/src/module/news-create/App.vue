<template>
  <div id="app">
    <heading></heading>
    <el-container>
      <el-aside width="18rem"><side-bar activated="3" class="side-bar"></side-bar></el-aside>
      <el-main>
        <el-form label-position="left" label-width="4rem" class="form-area" @submit.prevent :rules="rules" :model="news_info" ref="news-edit-form">
          <el-form-item label="标题:"  prop="news_title" >
            <el-input placeholder="请输入标题" v-model="news_info.news_title"></el-input>
          </el-form-item>
          <el-form-item label="正文:" prop="news_content">
            <el-input :autosize="{ minRows: 20, maxRows: 100}" placeholder="请输入正文" v-model="news_info.news_content" type="textarea"></el-input>
          </el-form-item>
        </el-form>
        <el-button class="save-button" @click="createNews"></el-button>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  import Heading from '../../components/Heading/Heading'
  import SideBar from "../../components/SideBar/SideBar"
  import Utils from "../../common/js/utils"

  export default {
    name: 'app',
    components: {
      SideBar,
      Heading
    },
    created(){
      let len = window.location.href.split('/').length
      let news_id = window.location.href.split('/')[len - 2].split('@')[1]
      if (news_id === "$") {
        this.new_news = true
        return
      }
      this.new_news = false
      Utils.get(this,'/a/news/detail?news_id='+news_id,null,function (_this,res) {
        if(res.code === 0){
          _this.$message.error("获取消息详情失败")
          Utils.setURL('news/')
        }
        _this.$set(_this.news_info,"news_title",res.data.news_title)
        _this.$set(_this.news_info,"news_content",res.data.news_content)
        _this.news_id = news_id
      })
    },
    data () {
      return {
        new_news:true,
        news_id:"",
        news_info:{
          news_title: "",
          news_content: ""
        },
        rules: {
          news_title:[{required: true, message: "请填写标题",trigger: 'blur'}],
          news_content: [{required: true, message: "请填写内容", trigger: 'blur'}]
        }
      }
    },
    methods: {
      createNews(){
        let _this = this
        this.$refs['news-edit-form'].validate(function (state, obj) {
          if (state) {
            if(_this.new_news){
              Utils.post(_this,"/a/news/create/",_this.news_info,function (_this,res) {
                if(res.code === 1)
                  Utils.setURL('news/')
                else
                  _this.$message.error("发布失败，请重试")
              })
            }
            else{
              Utils.get(_this,"/a/news/delete?news_id="+_this.news_id,null,function (_this,res) {
                if(res.code === 0)
                  _this.$message.error("删除失败，请重试")
                else{
                  Utils.post(_this,"/a/news/create/",_this.news_info,function (_this,res) {
                    if(res.code === 1)
                      Utils.setURL('news/')
                    else
                      _this.$message.error("删除成功，新建失败，请重试")
                  })
                }
              })
            }
          }
        })
      }
    }

  }
</script>

<style>
  .side-bar {
    margin-right: 1rem;
    min-width: 13rem;
  }

  .form-area {
    width: 50%;
    min-width: 50rem;
    margin-top: 5rem;
    margin-right: auto;
    margin-left: auto;
  }

  label {
    font-size: medium !important;
  }

  .save-button {
    width: 4rem;
    height: 4rem;
    border-radius: 4rem !important;
    background: #ffffff url("./images/save_icon.png") center center no-repeat !important;
    background-size: 2rem 2rem !important;
    box-shadow: 1px 1px 1px #888888;
    margin-left: 50% !important;
    margin-right: auto !important;
  }
</style>
