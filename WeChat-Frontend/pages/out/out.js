var util = require("../../utils/util.js")
// pages/out/out.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    s:true
  },

  handleGetMessage: function (e) {
    let msg = JSON.parse(e.detail.msg);
    if(msg["code"] != 1){
      util.msgPrompt("绑定失败",false);      
      return;
    }
    this.bindConfirm(msg["data"])
  },
  bindConfirm(data){
    app.bindConfirm(data,(res)=>{
      util.msgPrompt('绑定成功');
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let _this = this;
    app.getBindInfo({},(res)=>{
      if (res.data["data"]["permission"] == 0)
        _this.setData({s:false});
      else{
        setTimeout(() => {
          wx.navigateBack()
          util.msgPrompt('已绑定',false)  
        },500)

        
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})