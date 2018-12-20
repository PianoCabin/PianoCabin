//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  // handleGetMessage: function (e) {
  //   console.log(e.target.data)
  // },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function (e) {
    
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },
  goToOrderPage(){
    wx.navigateTo({
      url: '/pages/orderpage/orderpage',
    })
  },
  goToBindPage(){
    wx.navigateTo({
      url: '/pages/out/out',
    })
  },
  goToFeedback(){
    wx.navigateTo({
      url: '/pages/feedback/feedback',
    })
  },
  showNewsPage(event) {
    wx.navigateTo({
      url: '/pages/news/news',
    })
  }
})
