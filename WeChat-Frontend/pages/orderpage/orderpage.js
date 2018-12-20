//index.js
//获取应用实例
var util = require("../../utils/util.js")


const app = getApp()

Page({
  data: {
    order_list:[],
    order_status_list:['已取消','未支付','已支付','已完成'],
    cancel_reason_list:['未取消','预约超时','提前取消','琴房下线'],
    edit_view:false,
    classified:{},
    select_order_list:[],
    select_status:1,
    animation_data:null,
  },
  onReady(){
    this.getOrderList();
  },
  onShow(){
      this.getOrderList();
  },
  getOrderList(){
    app.getOrderList({},this.updateOrderList);
  },
  updateOrderList(res){
    let data_list = res.data["data"]["order_list"]
    let new_list = [];
    let new_cancel_list = [];
    let new_unpaid_list = [];
    let new_paid_list = [];
    let new_complete_list = [];
    let new_classified = {}
    for (let i = 0; i < Object.keys(this.data.order_status_list).length; i++) {
      new_classified[i] = [];
    }
    for(let i = 0;i<data_list.length;i++){
      let order = {};
      order["piano_type"] = data_list[i]["brand"];
      order["room_num"] = data_list[i]["room_num"];
      order["price"] = data_list[i]["price"];
      order["start_time"] = util.timestampToTimeString(data_list[i]["start_time"] * 1000);
      order["end_time"] = util.timestampToTimeString(data_list[i]["end_time"]*1000);
      order["order_date"] = util.timestampToDateString(data_list[i]["start_time"] * 1000);
      order["order_status"] = this.data.order_status_list[data_list[i]["order_status"]];
      order["status"] = data_list[i]["order_status"];
      order["cancel_reason"] = data_list[i]["cancel_reason"];
      if(order["status"] == 0)
        order["order_status"] = this.data.cancel_reason_list[data_list[i]["cancel_reason"]];
      order["order_id"] = data_list[i]["order_id"];
      order["index"] = i;
      new_list.push(order);
      new_classified[order["status"]].push(order)
    }
    this.setData({
      order_list:new_list,
      cancel_list:new_cancel_list,
      unpaid_list:new_unpaid_list,
      paid_list:new_paid_list,
      complete_list:new_complete_list,
      classified:new_classified,
    });
    this.setData({
      select_order_list: this.data.classified[this.data.select_status]
    })
    console.log("cancel_list");
    console.log(this.data.cancel_list)
    console.log("classified")
    console.log(this.data.classified);
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
    wx.navigateTo({
      url: '/pages/orderinfo/orderinfo?order_id='+order_id.toString(),
    })
  },
  orderType(event){
    let new_type = event.currentTarget.id;
    this.setData({
      select_status:new_type,
      select_order_list:this.data.classified[new_type]
    })
  },
  onPullDownRefresh(){
    this.getOrderList()
  }
})
