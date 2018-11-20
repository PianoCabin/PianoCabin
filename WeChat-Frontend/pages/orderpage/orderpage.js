//index.js
//获取应用实例
var util = require("../../utils/util.js")


const app = getApp()

Page({
  data: {
    order_list:[],
    order_status_list:['已取消','未支付','已支付','已完成'],
    edit_view:false,
    animation_data:null,
  },
  onReady(){
  },
  onShow(){
      this.getOrderList();
  },
  getOrderList(){
    app.getOrderList({},this.updateOrderList);
  },
  updateOrderList(data_list){
    let new_list = [];
    for(let i = 0;i<data_list.length;i++){
      let order = {};
      order["piano_type"] = data_list[i]["piano_type"];
      order["room_num"] = data_list[i]["room_num"];
      order["price"] = data_list[i]["price"];
      order["start_time"] = util.timestampToTimeString(data_list[i]["start_time"] * 1000);
      order["end_time"] = util.timestampToTimeString(data_list[i]["end_time"]*1000);
      order["order_date"] = util.timestampToDateString(data_list[i]["start_time"] * 1000);
      order["order_status"] = this.data.order_status_list[data_list[i]["order_status"]];
      order["status"] = data_list[i]["order_status"];
      order["order_id"] = data_list[i]["order_id"];
      order["index"] = i;
      new_list.push(order);
    }
    this.setData({
      order_list:new_list
    });
  },
  editOrder(event){
    this.showEditView()
  },
  toUserPage(){
    wx.switchTab({
      url: '/pages/userpage/userpage',
    })
  },
  orderDetail(event){
    let order_id = this.data.order_list[event.currentTarget.id]["order_id"]
    console.log(order_id);
    wx.navigateTo({
      url: '/pages/orderinfo/orderinfo?order_id='+order_id.toString(),
    })
  }
})
