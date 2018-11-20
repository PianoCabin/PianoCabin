// pages/orderinfo/orderinfo.js

var util = require("../../utils/util.js")

const app = getApp()


const OrderStatus = ["已取消",'未付款','已付款','已完成']


Page({

  /**
   * 页面的初始数据
   */
  data: {
    info:{},
    edit:false,
    min_order:60*60*1000,
    min_interval:10*60*1000,
    starttime_list:[],
    endtime_list:[],
    cur_date:"",
    roominfo:{},
    animation_data: null,
    cancel_view:false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let order_id = options.order_id;
    this.getOrderInfo(order_id);
    console.log((new Date()).getMonth());
    this.setData({
      cur_date:new Date().toLocaleDateString()
    })
  },
  getOrderInfo(order_id){
    wx.request({
      url: app.globalData.backend+`/u/order/list`,
      data:{
        order_id:order_id
      },
      success:res =>{
        console.log(res);
        if(res.data['code'] == 1)
        {
          this.updateOrderInfo(res.data['data']["order_list"][0])
        }
        else
          util.msgPrompt(res.data['msg'])
      },
      fail:res =>{
        util.msgPrompt("get info fail");
      }
    })
  },
  updateOrderInfo(data){
    let info = {};
    info["piano_type"] = data["piano_type"];
    info["room_num"] = data["room_num"];
    info["price"] = data["price"];
    info["order_status"] = OrderStatus[data["order_status"]];
    info["order_id"] = data["order_id"];
    info["status"] = data["order_status"];
    info["user_id"] = app.globalData.user_session;
    info["date"] = util.timestampToDateString(data['start_time']*1000);
    info["start_time"] = data["start_time"] * 1000;
    info["end_time"] = data["end_time"]*1000;
    info["order_start"] = util.timestampToTimeString(data['start_time'] * 1000);
    info["order_end"] = util.timestampToTimeString(data['end_time'] * 1000);
    info["user_id"] = data["user_id"];
    info["qrcode"] = data["qrcode"];
    
    this.setData({
      info:info,
      start_time: util.timestampToTimeString(data["start_time"] * 1000),
      end_time:util.timestampToTimeString(data["end_time"]*1000),
    })
    if (data["order_status"] == 1)
      this.getRoomInfo(data["room_num"]);
  },
  getRoomInfo(room_num){
    let today = new Date()
    today.setHours(12,0,0,0);
    wx.request({
      url: app.globalData.backend + `/u/order/piano-rooms-list/`,
      data:{
        Authorization:app.globalData.user_session,
        room_num:room_num,
        date:today.getTime()
      },
      method:"POST",
      success:res =>{
        console.log(res.data);
        this.setStartList(res.data["data"]["room_list"][0]);
        this.setData({
          roominfo: res.data['data']["room_list"][0]
        })
      }
    })

  },
  setStartList(room_info){
    let transer = new Date()
    transer.setHours(12,0,0,0)
    let start = transer.getTime();
    transer.setHours(22,30,0,0);
    let end = transer.getTime();
    let start_list=[];

    let orders = room_info["occupied_time"];

    console.log("ordersold:");
    console.log(orders);
    for (let i = 0; i < orders.length; i++) {
      orders[i][0] *= 1000;
      orders[i][1] *= 1000;
      if (orders[i][0] == this.data.info["start_time"] && orders[i][1] == this.data.info["end_time"]){
        orders.splice(i,1);
      }
    }
    console.log("orders");
    console.log(orders);

    for (let i = 0; i < orders.length; i++) {
      //查找每一段时长大于min_order的空闲时间
      console.log(orders[i][0]);
      console.log(start);
      if (orders[i][0] - start >= this.data.min_order) {
        let ss = orders[i][0];
        //如果找到满足的空闲时长，按照间隔取开始时间，将满足的时间都加入开始时间列表
        while (ss - start >= this.data.min_order) {
          let tt = new Date(start);
          let startable = util.timestampToTimeString(tt);
          start_list.push(startable);
          start = start + this.data.min_interval;
        }
      }
      start = orders[i][1];
      
    }

    //在最后一个预约与开放结束之间的空闲时间在以上的循环中被遗漏了，在此补上
    transer.setHours(12,0,0,0)
    let ss = transer.getTime();
    if(orders.length>0)
      ss = orders[orders.length - 1][1];

    console.log(ss);
    while (end - ss >= this.data.min_order) {
      let tt = new Date(ss);
      let startable = util.timestampToTimeString(tt);
      start_list.push(startable);
      ss = ss + this.data.min_interval;
    }
    console.log(start_list);
    this.setData({ starttime_list: start_list,edit:true });
  },
  
  setOrderStart(event) {
    let info = this.data.info;
    let end_list = [];
    let index = event.detail["value"];
    let room_info = this.data.roominfo;

    let list = this.data.starttime_list[index].split(":");
    let transer = new Date()
    transer.setHours(22, 30, 0, 0)
    let start = new Date(util.timeStringToTimestamp(this.data.cur_date, this.data.starttime_list[index]));
    let max_end = transer.getTime();

    console.log("setOrderStart");
    console.log(room_info["occupied_time"]);
    for (let i = 0; i < room_info["occupied_time"].length; i++) {
      if (start <= room_info["occupied_time"][i][0]) {
        max_end = room_info["occupied_time"][i][0];
        console.log("here");
        break;
      }
      if (i == room_info["occupied_time"].length - 1) {
        transer.setHours(22,30,0,0)
        max_end = transer.getTime();
      }
    }
    start = start.getTime() + this.data.min_order;
    while (start <= max_end) {
      end_list.push(util.timestampToTimeString(start));
      start = start + this.data.min_interval;
    }
    info["order_start"] = this.data.starttime_list[index];
    info["order_end"] = "结束";
    info["price"] = "";
    this.setData({ endtime_list: end_list, info: info, start_time: info["order_start"],end_time:info['order_end']});
  },
  setOrderEnd(event){
    let index = event.detail["value"];
    let start = util.timeStringToTimestamp(this.data.cur_date,this.data.start_time);
    let end = util.timeStringToTimestamp(this.data.cur_date,this.data.endtime_list[index]);
    let hours = parseInt((end - start) / (60 * 60 * 1000)) + ((end - start) % (60 * 60 * 1000)>0);
    let newprice = hours*this.data.roominfo["unit_price"];
    let info = this.data.info;
    info["price"] = newprice;
    info["order_end"] = this.data.endtime_list[index];
    this.setData({
      end_time:info["order_end"],
      info:info
    })
  },
  toOrderPage(){
    wx.redirectTo({
      url: '/pages/orderpage/orderpage',
    })
  },
  changeOrder(){
    let info = this.getInfoObject();
    info["Authorization"] = app.globalData.user_session,
    console.log(info);
    wx.request({
      url: app.globalData.backend +`/u/order/change/`,
      data:info,
      method:"POST",
      success: res =>{
        console.log(res);
      },
      fail:res =>{
        console.log(res);
      }
    })
  },
  cancelOrder(){
    wx.request({
      url: app.globalData.backend + `/u/order/cancel/`,
      data: {
        Authorization:app.globalData.user_session,
        order_id:this.data.info["order_id"]
      },
      method: "POST",
      success: res => {
        console.log(res);
        wx.redirectTo({
          url: '/pages/orderpage/orderpage',
        })
      },
      fail: res => {
        console.log(res);
      }
    })
  },
  checkCancelOrder(){
    this.showCancelView();
  },
  getInfoObject(){
    let info = {}
    info["room_num"] = this.data.info["room_num"];
    info["start_time"] = util.timeStringToTimestamp(this.data.info["date"], this.data.info["order_start"]) / 1000;
    info["end_time"] = util.timeStringToTimestamp(this.data.info["date"], this.data.info["order_end"]) / 1000;
    info["price"] = this.data.info["price"];
    info["order_id"] = this.data.info["order_id"];
    console.log(info);
    return info
  },
  showCancelView() {
    var animation = wx.createAnimation({
      duration: 250,
      timingFunction: "linear",
      delay: 0
    });

    this.animation = animation;

    animation.opacity(0).rotateX(-100).step();

    this.setData({
      animation_data: animation.export(),
    })
    setTimeout(function () {
      animation.opacity(1).rotateX(0).step();
      this.setData({
        animation_data: animation,
      })
    }.bind(this), 100)
    this.setData({ cancel_view: true });
  },
  hideCancelView() {
    var animation = wx.createAnimation({
      duration: 250,
      timingFunction: "linear",
      delay: 0
    });

    this.animation = animation;

    animation.opacity(0).rotateX(-100).step();

    this.setData({
      animation_data: animation.export(),
    })
    setTimeout(function () {
      animation.opacity(1).rotateX(0).step();
      this.setData({
        animation_data: animation,
        cancel_view: false
      })
    }.bind(this), 100)
  },
})