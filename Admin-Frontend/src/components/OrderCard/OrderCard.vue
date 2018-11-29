<!--部件用作订单卡片-->
<template>
    <div id="order-card">
      <el-card class="box-card">
        <el-row>
          <el-col :span="3" class="image-div">
            <div><img class="image" src="../../module/order/images/room_icon.png"/></div>
          </el-col>
          <el-col :span="5">
            <div class="head-div">
              <h1><slot name="brand"></slot></h1>
              <h3 class="room-num"><slot name="room-num"></slot></h3>
            </div>
          </el-col>
          <el-col :span="12">
            <div>
              <p>预约人： &nbsp&nbsp<slot name="user-id"></slot></p>
              <p>订单编号：<slot name="order-id"></slot></p>
              <p>预约时间：<slot name="order-time"></slot></p>
              <p>创建时间：<slot name="create-time"></slot></p>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="state-div">
              <p class="order-state"><slot name="order-state"></slot></p>
              <p class="price-text">预约金额：￥<slot name="price"></slot></p>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </div>
</template>

<script>
    export default {
        name: "order-card"
    }
</script>

<style scoped>
  .image-div {
    margin-top: 3rem !important;
  }

  .head-div {
    margin-top: 3rem !important;
  }

  .state-div {
    margin-top: 2rem !important;
    font-size: medium !important;
  }

  .image {
    height: 3rem;
    margin-left: 2rem !important;
  }

  .price-text {
    margin-top: 3rem;
    color: #7D7979;
  }

  .order-state, .room-num {
    color: #7D7979;
  }
</style>
