var config = require('../config')
if (!process.env.NODE_ENV) process.env.NODE_ENV = config.dev.env
var path = require('path')
var express = require('express')
var bodyParser = require("body-parser");
var webpack = require('webpack')
var opn = require('opn')
var proxyMiddleware = require('http-proxy-middleware')
var webpackConfig = require('./webpack.dev.conf')

// default port where dev server listens for incoming traffic
var port = process.env.PORT || config.dev.port
// Define HTTP proxies to your custom API backend
// https://github.com/chimurai/http-proxy-middleware
var proxyTable = config.dev.proxyTable

var app = express()
var compiler = webpack(webpackConfig)

var devMiddleware = require('webpack-dev-middleware')(compiler, {
  publicPath: webpackConfig.output.publicPath,
  stats: {
    colors: true,
    chunks: false
  }
})

var hotMiddleware = require('webpack-hot-middleware')(compiler)
// force page reload when html-webpack-plugin template changes
compiler.plugin('compilation', function (compilation) {
  compilation.plugin('html-webpack-plugin-after-emit', function (data, cb) {
    hotMiddleware.publish({ action: 'reload' })
    cb()
  })
})

// proxy api requests
Object.keys(proxyTable).forEach(function (context) {
  var options = proxyTable[context]
  if (typeof options === 'string') {
    options = { target: options }
  }
  app.use(proxyMiddleware(context, options))
})

// handle fallback for HTML5 history API
app.use(require('connect-history-api-fallback')())
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))

// serve webpack bundle output
app.use(devMiddleware)

// enable hot-reload and state-preserving
// compilation error display
app.use(hotMiddleware)

// serve pure static assets
var staticPath = path.posix.join(config.dev.assetsPublicPath, config.dev.assetsSubDirectory)
app.use(staticPath, express.static('./static'))

app.post('/a/login', (req, res, next) => {
  let username = req.body.username;
  let password = req.body.password;
  if (!(username === "123" && password === "456")) {
    res.json({
      code: 0,
      message: 'failed',
      data: 'login'
    })
  }
  else {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
  }
});

app.post('/a/logout', (req, res, next) => {
  res.json({
      code: 1,
      message: 'success',
    })
});

app.post('/a/piano-room/delete', (req, res, next) => {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
});

app.post('/a/piano-room/create', (req, res, next) => {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
});

app.post('/a/piano-room/edit', (req, res, next) => {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
});

app.post('/a/news/create', (req, res, next) => {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
});

app.post('/a/news/delete', (req, res, next) => {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
});

app.post('/a/piano-room/detail', (req, res, next) =>{
  res.json({
    code: 1,
    data: {
      room_num: '404',
      brand: '大猪蹄子',
      piano_type: '林老师',
      price_0: '0',
      price_1: '0',
      price_2: '-1',
      is_online: '上线',
      art_ensemble: '否'
    }
  })
})

app.post('/a/piano-room/list', (req, res, next) => {
  let piano_type = req.body.piano_type;
  if (piano_type === '钢琴') {
    res.json({
      code: 1,
      message: 'success',
      data: {
        room_list: {
          '星海立式钢琴': [
            {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            },
            {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            }
          ],
          '卡瓦伊立式钢琴': [
            {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            },
            {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            }
          ],
          '雅马哈立式钢琴': [
            {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            },
            {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            }
          ]
        }
      }
    })
  }
  else if (piano_type === '电子琴') {
    res.json({
      code: 1,
      message: 'success',
      data: {
        room_list: {
          '电子琴': [
            {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            }, {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            },
            {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            }, {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            },
            {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            }
          ]
        }
      }
    })
  }
  else {
    res.json({
      code: 1,
      message: 'success',
      data: {
        room_list: {
          '小琴屋': [
            {
              room_num: '404',
              brand: '大猪蹄子',
              piano_type: '林老师',
              price_0: 0,
              price_1: 0,
              price_2: -1,
              online: 1,
              art_ensemble: 1
            }
          ]
        }
      }
    })
  }
})

app.get('/a/news/list', (req, res, next) => {
  res.json({
    code: 1,
    data: {
      news_list:[
      {
        news_title: '林老师是大猪蹄子',
        publish_time: '23333',
        news_id: '20160132xx'
      },
      {
        news_title: '林老师是大猪蹄子',
        publish_time: '23333',
        news_id: '20160132xx'
      },
      {
        news_title: '林老师是大猪蹄子',
        publish_time: '23333',
        news_id: '20160132xx'
      }
    ]
    }
  })
})

app.get('/a/news/detail', (req, res, next) =>{
  res.json({
    code: 1,
    data: {
      news_title: '404',
      news_content: '大猪蹄子',
      publish_time: '0'
    }
  })
})

app.post('/a/order/list', (req, res, next) => {
  let order_status = req.body.order_status;
  if (order_status == 1) {
    res.json({
      code: 1,
      message: 'success',
      data: {
        order_list: [
            {
              room_num: '404',
              brand: '大猪蹄子',
              user_id: 0,
              start_time : 0,
              end_time: -1,
              price: 1,
              order_status: '未完成'
            },
            {
              room_num: '404',
              brand: '猪蹄子',
              user_id: 0,
              start_time : 0,
              end_time: -1,
              price: 1,
              order_status: '未完成'
            }
          ]
      }
    })
  }
  else if (order_status == 2) {
    res.json({
      code: 1,
      message: 'success',
      data: {
        order_list: [
            {
              room_num: '404',
              brand: '大猪蹄子',
              user_id: 0,
              start_time : 0,
              end_time: -1,
              price: 1,
              order_status: '已完成'
            },
            {
              room_num: '404',
              brand: '猪蹄子',
              user_id: 0,
              start_time : 0,
              end_time: -1,
              price: 1,
              order_status: '已完成'
            },
            {
              room_num: '404',
              brand: '猪蹄子',
              user_id: 0,
              start_time : 0,
              end_time: -1,
              price: 1,
              order_status: '已完成'
            }
          ]
      }
    })
  }
  else {
    res.json({
      code: 1,
      message: 'success',
      data: {
        order_list: [
          {
              room_num: '404',
              brand: '猪蹄子',
              user_id: 0,
              start_time : 0,
              end_time: -1,
              price: 1,
              order_status: '已取消'
          }
          ]
      }
    })
  }
})

app.get('/a/feedback/list', (req, res, next) => {
  let read_status = req.param.read_status;
  if (read_status == 0) {
    res.json({
      code: 1,
      message: 'success',
      data: {
        feedback_list : [
            {
              feedback_title: '林老师是大猪蹄子',
              feedback_id: '0001',
              user_id: '20160132xx',
              time : 0
            },
            {
              feedback_title: '林老师是大猪蹄子',
              feedback_id: '0002',
              user_id: '20162333xx',
              time : 0
            }
          ]
      }
    })
  }
  else {
    res.json({
      code: 1,
      message: 'success',
      data: {
        feedback_list : [
            {
              feedback_title: '大猪蹄子是林老师',
              feedback_id: '0001',
              user_id: '20160132xx',
              time : 0
            },
            {
              feedback_title: '大猪蹄子是林老师',
              feedback_id: '0001',
              user_id: '20160132xx',
              time : 0
            },
            {
              feedback_title: '大猪蹄子是林老师',
              feedback_id: '0002',
              user_id: '20162333xx',
              time : 0
            }
          ]
      }
    })
  }
})

app.get('/a/feedback/detail', (req, res, next) =>{
  res.json({
    code: 1,
    data: {
      feedback_title: '林老师是大猪蹄子',
      feedback_content: '林老师是大猪蹄子林老师是大猪蹄子林老师是大猪蹄子',
      publish_time: '23333',
      user_id: '20160132xx'
    }
  })
})

app.get('/a/login', (req, res, next) => {
  res.json({
    code: 0,
    message: 'success',
    data: ''
  })
});

app.post('/a/piano-room/edit', (req, res, next) => {
  res.json({
    code: 1,
    message: 'success',
    data: ''
  })
});

app.post('/a/piano-room/create', (req, res, next) => {
  res.json({
    code: 1,
    message: 'success',
    data: ''
  })
});

app.get('/a/user/update', (req, res, next) => {
  res.json({
    code: 1,
    message: 'success',
    data: ''
  })
});

module.exports = app.listen(port, function (err) {
  if (err) {
    console.log(err)
    return
  }
  var uri = 'http://localhost:' + port
  console.log('Listening at ' + uri + '\n')
  opn(uri)
})
