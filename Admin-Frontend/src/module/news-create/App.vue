<template>
  <div id="app">
    <heading></heading>
    <el-container>
      <el-aside width="18rem"><side-bar activated="3" class="side-bar"></side-bar></el-aside>
      <el-main>
        <el-form label-position="left" label-width="3rem" class="form-area">
          <el-form-item label="标题:"><el-input placeholder="请输入标题"></el-input></el-form-item>
          <el-form-item label="正文:"><el-input :autosize="{ minRows: 20, maxRows: 100}" placeholder="请输入正文" type="textarea"></el-input></el-form-item>
        </el-form>
        <el-button class="save-button"></el-button>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  import Heading from '../../components/Heading/Heading'
  import SideBar from "../../components/SideBar/SideBar"
  export default {
    name: 'app',
    components: {
      SideBar,
      Heading
    },
    data () {
      return {
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
