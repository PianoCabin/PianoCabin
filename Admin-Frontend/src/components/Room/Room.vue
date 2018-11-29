<!--部件用作room页面房间按钮-->
<template>
    <div id="room" @click.prevent="clickEvent">
      <el-container :body-style="{ padding: '0px' }">
        <el-header><img src="../../module/order/images/room_icon.png" class="image"></el-header>
        <el-main style="padding: 14px;" class="text">
          <span id="room-num"><slot name="room-num"></slot></span>
        </el-main>
      </el-container>
    </div>
</template>

<script>
    export default {
        name: "room",
        methods: {
          clickEvent: function () {
            let target = event.currentTarget
            let room_num = target.getElementsByTagName('span')[0].innerText
            this.$emit("click", room_num)
          }
        }
    }
</script>

<style scoped>
  .image {
    width: 60%;
    margin-left: auto !important;
    margin-right: auto !important;
    display: block;
  }

  .text {
    text-align: center;
    margin-top: 1rem;
  }
</style>
