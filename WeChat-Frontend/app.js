var util = require("utils/util.js")

//app.js
let app = App({
  onLaunch: function () {
    try {
      this.globalData.user_session = wx.getStorageSync("user_session");
    }
    catch (e) {
      console.log("wrong when get local storage");
    }
    if (!this.globalData.user_session) {
      this.getUserSession(() => { });
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
  getUserSession(callback, arg1 = null, arg2 = null, arg3 = null, arg4 = null) {
    wx.login({
      success: res => {
        console.log("we.login return ");
        console.log(res);
        wx.request({
          url: this.globalData.backend + `/u/login/`,
          method: "POST",
          data: {
            code: res.code
          },
          success: res => {
            console.log("paino session return ");
            console.log(res);
            if (res.data["code"] == 1) {
              this.globalData.user_session = res.data["data"]["session"];
              wx.setStorageSync("user_session", this.globalData.user_session);
              console.log("get from net");
              console.log(this.globalData.user_session);
              callback(arg1, arg2, arg3, arg4);
            }
            else {
              util.msgPrompt(res.data["msg"]);
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
  getRoomList(data, successFunc) {
    this._post('/u/order/piano-rooms-list/', data, successFunc)
  },
  submitOrder(data, successFunc) {
    this._post(`/u/order/normal/`, data, successFunc)
  },
  getOrderList(data, successFunc) {
    this._get(`/u/order/list`, data, successFunc)
  },
  changeOrder(data, successFunc) {
    this._post(`/u/order/change/`, data, successFunc)
  },
  cancelOrder(data, successFunc) {
    this._post(`/u/order/cancel/`, data, successFunc)
  },
  feedback(data,successFunc){
    this._post(`/u/feedback/`,data,successFunc)
  },
  getNewsList(data,successFunc){
    this._post(`/u/news/list/`,data,successFunc)
  },
  getPayMsg(data,successFunc){
    this._post(`/u/order/pay/`,data,successFunc)
  },
  payForOrder(timestamp, nonce_str, prepare_id, sign) {
    console.log(timestamp);
    console.log(nonce_str);
    console.log(prepare_id);
    console.log(sign);


    wx.requestPayment({
      timeStamp: timestamp,
      nonceStr: nonce_str,
      package: prepare_id,
      signType: 'MD5',
      paySign: sign,
      success: function (res) {
        console.log("支付成功!");
        console.log(res);
        util.msgPrompt('支付成功!');
        wx.navigateTo({
          url: '/pages/orderpage/orderpage',
        })
      },
      fail: function (res) {
        console.log("支付失败!!");
        console.log(res);
        util.msgPrompt('支付失败!!');
        // wx.navigateTo({
        //   url: '/pages/orderpage/orderpage',
        // })
      }
    })
  },
  _post(url, data, successFunc = res => { console.log(res) }, failFunc = res => { console.log(res) }) {
    if (this.globalData.user_session) {
      let _this = this;
      this.globalData.network_busy = true;
      setTimeout(() => {
        if (_this.globalData.network_busy)
          wx.showLoading({
            title: 'loading',
          })
      }, this.globalData.network_waiting)
      console.log(url + "   data:");
      console.log(data);
      console.log("session: " + this.globalData.user_session)
      wx.request({
        url: this.globalData.backend + url,
        data: data,
        header: {
          "Authorization": this.globalData.user_session
        },
        method: "POST",
        success: res => {
          console.log(url + "   return:");
          console.log(res);
          if (res.data["code"] == 0)
            util.msgPrompt(res.data["msg"]);
          else
            successFunc(res);
        },
        fail: res => {
          failFunc(res);
        },
        complete: res => {
          this.globalData.network_busy = false;
          wx.hideLoading()
        }
      })
    }
    else {
      this.getUserSession(this._post, url, data, successFunc, failFunc);
    }
  },
  _get(url, data, successFunc = res => { console.log(res) }, failFunc = res => { console.log(res) }) {
    if (this.globalData.user_session) {
      let _this = this;
      this.globalData.network_busy = true;
      setTimeout(() => {
        if (_this.globalData.network_busy)
          wx.showLoading({
            title: 'loading',
          })
      }, this.globalData.network_waiting)
      console.log(url + "   data:");
      console.log(data);
      console.log("session: " + this.globalData.user_session)
      wx.request({
        url: this.globalData.backend + url,
        data: data,
        header: {
          "Authorization": this.globalData.user_session
        },
        method: "GET",
        success: res => {
          console.log(url + "   return:");
          console.log(res);
          if (res.data["code"] == 0)
            util.msgPrompt(res.data["msg"]);
          else
            successFunc(res);
        },
        fail: res => {
          failFunc(res);
        },
        complete: res => {
          this.globalData.network_busy = false;
          wx.hideLoading()
        }
      })
    }
    else
      this.getUserSession(this._get, url, data, successFunc, failFunc)
  },
  
  globalData: {
    userInfo: null,
    user_session: null,
    user_nickname: "默认用户",
    // backend: `https://711602.iterator-traits.com`,
    backend: `http://127.0.0.1:80`,
    // backend: `https://0a8bba0a.ngrok.io`,
    user_session: null,
    network_waiting:0
  }
})


module.exports = app;