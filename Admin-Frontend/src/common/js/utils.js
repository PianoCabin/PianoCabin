class Utils {
  // 工具类

  // 页面跳转
  static setURL(url) {
    // 测试用
    // window.location.href = window.location.protocol + '//' + window.location.host + '/module' + '/' + url.replace('/','') + '.html'
    console.log(url)
    window.location.href = window.location.protocol + '//' + window.location.host + '/' + url
  }

  // 根据api生成完整地址
  static getURL(url) {
    //测试用
    // return 'http://127.0.0.1:8000' + url
    return window.location.protocol + '//' + window.location.host + '/' + url
  }

  // post请求
  static post(_this, api, data, callback) {
    //测试用
    // api = Utils.getURL(api)

    _this.$http.post(api, data).then(response => {
      let res = response.body
      if (res.code === 0 && res.msg === "not login") {
        Utils.setURL("login/")
        return
      }
      callback(_this, res)
    }, response => {
      _this.$message.error('服务器出错')
    })
  }

  // get请求
  static get(_this, api, data=null, callback) {
    //测试用
    // api = Utils.getURL(api)

    _this.$http.get(api, data).then(response => {
      let res = response.body
      callback(_this, res)
    }, response => {
      _this.$message.error('服务器出错')
    })
  }
}

export default Utils
