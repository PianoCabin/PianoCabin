var util = require("utils/util.js")

//app.js
App({
  onLaunch: function () {
    try {
      this.globalData.user_session = wx.getStorageSync("user_session");
    }
    catch (e) {
      console.log("wrong when get local storage");
    }
    if (!this.globalData.user_session) {
      this.getUserSession();
    }
    else {
      console.log("in storage");
      console.log(this.globalData.user_session);
    }

    // // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  getUserSession: function () {
    wx.login({
      success: res => {
        console.log(res);
        wx.request({
          url: this.globalData.backend + `/u/login/`,
          method: "POST",
          data: {
            code: res.code
          },
          success: res => {
            if (res.data["code"] == 1) {
              this.globalData.user_session = res.data["data"]["session"];
              wx.setStorageSync("user_session", this.globalData.user_session);
              console.log("get from net");
              console.log(this.globalData.user_session);
            }
          },
          fail: res => {
            util.msgPrompt("get session failed");
          }
        })
      },
      fail: res => {
        util.msgPrompt("login failed");
      }
    })
  },
  globalData: {
    userInfo: null,
    user_session: null,
    // backend:`https://711602.iterator-traits.com`,
    backend: `http://127.0.0.1:80`,
    user_session: null
  }
})