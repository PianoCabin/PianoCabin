var util = require("utils/util.js")

//app.js
App({
  onLaunch: function () {
    try{
      this.globalData.user_session = wx.getStorageSync("user_session");
    }
    catch(e){
      console.log("wrong when get local storage");
    }
    if(!this.globalData.user_session){
      this.getUserSession(()=>{});
    }
    else{
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
              this.globalData.user_nickname = res.userInfo.nickName;

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
  getUserSession: function(callback,arg1=null,arg2=null){
    wx.login({
      success: res => {
        wx.request({
          url: this.globalData.backend + `/u/login/`,
          method: "POST",
          data: {
            code: res.code
          },
          success: res => {
            if (res.data["code"] == 1) {
              this.globalData.user_session =  res.data["data"]["session"];
              wx.setStorageSync("user_session", this.globalData.user_session);
              console.log("get from net");
              console .log(this.globalData.user_session);
              callback(arg1,arg2);
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
  getRoomList(data,successFunc,...args){
    console.log("getRoomlist-data:");
    console.log(data);
    console.log(successFunc);
    if(this.globalData.user_session)
    {
      wx.request({
        url: this.globalData.backend + '/u/order/piano-rooms-list/',
        data: data,
        header: {
          "Authorization": this.globalData.user_session
        },
        method: "POST",
        success: res => {
          if (res.data["code"] == 0) {
            util.msgPrompt(res.data["msg"]);
          }
          else {
            console.log("getRoomList-return:");
            console.log(res);
            successFunc(res);
          }
        },
        fail: res => {
          util.msgPrompt("network wrong");
        }
      })
    }
    else{
      this.getUserSession(this.getRoomList,data,successFunc);
    }
  },
  submitOrder(data,successFunc){

    console.log("submitOrder-data:");
    console.log(data);
    wx.request({
      url: this.globalData.backend + `/u/order/normal/`,
      method: "POST",
      data: data,
      header: {
        "Authorization": this.globalData.user_session
      },
      success: function (res) {
        if (res.data["code"] == 0) {
          util.msgPrompt(res.data["msg"]);
        }
        else {
          console.log("submitOrder-return:")
          console.log(res);
          successFunc(res);
        }
      },
      fail: function (res) {
        console.log("net work wrong");
      }
    })
  },
  getOrderList(data,successFunc) {
    console.log("getOrderList-data:");
    console.log(data);
    console.log("usersession:"+this.globalData.user_session);
    if (this.globalData.user_session) {
      wx.request({
        url: this.globalData.backend + `/u/order/list`,
        method: "GET",
        header: {
          "Authorization": this.globalData.user_session
        },
        data:data,
        success: res => {
          if (res.data["code"] == 1) {
            console.log("getOrderList-return-list:")
            console.log(res.data["data"]["order_list"])
            successFunc(res.data["data"]["order_list"])
          }
          else {
            console.log(res);
          }
        },
        fail: res => {
          util.msgPrompt("network wrong");
        }
      })
    }
    else{
      this.getUserSession(this.getOrderList(data, successFunc) )
    }
  },
  changeOrder(data,successFunc){
    console.log("changeOrder-data:");
    console.log(data);
    wx.request({
      url: this.globalData.backend + `/u/order/change/`,
      data: data,
      header: {
        "Authorization": this.globalData.user_session
      },
      method: "POST",
      success: res => {
        console.log("changeOrder-return");
        console.log(res);
        successFunc(res)
      },
      fail: res => {
        console.log(res);
      }
    })
  },
  cancelOrder(data,successFunc){
    console.log("cancelOrder-data:");
    console.log(data);
    wx.request({
      url: this.globalData.backend + `/u/order/cancel/`,

      data: data,
      header: {
        "Authorization": this.globalData.user_session
      },
      method: "POST",
      success: res => {
        console.log("cancelOrder-return");
        console.log(res);
        successFunc(res);
      },
      fail: res => {
        console.log(res);
      }
    })
  },
  globalData: {
    userInfo: null,
    user_session:null,
    user_nickname:"默认用户",
    backend:`https://711602.iterator-traits.com`,
    // backend: `http://127.0.0.1:80`,
    // backend:`http://f23e7fdc.ngrok.io`,
    user_session:null
  }
})