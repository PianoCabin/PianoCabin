'use strict'
const utils = require('./utils')
const webpack = require('webpack')
const config = require('../config')
const merge = require('webpack-merge')
const path = require('path')
const baseWebpackConfig = require('./webpack.base.conf')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin')
const portfinder = require('portfinder')

const HOST = process.env.HOST
const PORT = process.env.PORT && Number(process.env.PORT)

const express = require('express');
const bodyParser = require("body-parser");
const app = express();
const Router = express.Router();

Router.post('/a/login', (req, res, next) => {
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

Router.post('/a/logout', (req, res, next) => {
  res.json({
      code: 1,
      message: 'success',
    })
});

Router.post('/a/piano-room/delete', (req, res, next) => {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
});

Router.post('/a/piano-room/create', (req, res, next) => {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
});

Router.post('/a/piano-room/edit', (req, res, next) => {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
});

Router.post('/a/news/create', (req, res, next) => {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
});

Router.post('/a/news/delete', (req, res, next) => {
    res.json({
      code: 1,
      message: 'success',
      data: 'login'
    })
});

Router.post('/a/piano-room/detail', (req, res, next) =>{
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

Router.post('/a/piano-room/list', (req, res, next) => {
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

Router.get('/a/news/list', (req, res, next) => {
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

Router.get('/a/news/detail', (req, res, next) =>{
  res.json({
    code: 1,
    data: {
      news_title: '404',
      news_content: '大猪蹄子',
      publish_time: '0'
    }
  })
})

Router.post('/a/order/list', (req, res, next) => {
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

Router.get('/a/feedback/list', (req, res, next) => {
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

Router.get('/a/feedback/detail', (req, res, next) =>{
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

Router.get('/a/login', (req, res, next) => {
  res.json({
    code: 1,
    message: 'success',
    data: ''
  })
});

Router.post('/a/piano-room/edit', (req, res, next) => {
  res.json({
    code: 1,
    message: 'success',
    data: ''
  })
});

Router.post('/a/piano-room/create', (req, res, next) => {
  res.json({
    code: 1,
    message: 'success',
    data: ''
  })
});

Router.get('/a/user/update', (req, res, next) => {
  res.json({
    code: 1,
    message: 'success',
    data: ''
  })
});

const devWebpackConfig = merge(baseWebpackConfig, {
  module: {
    rules: utils.styleLoaders({ sourceMap: config.dev.cssSourceMap, usePostCSS: true })
  },
  // cheap-module-eval-source-map is faster for development
  devtool: config.dev.devtool,

  // these devServer options should be customized in /config/index.js
  devServer: {
    before(app) {
      app.use(bodyParser.urlencoded({ extended: false }))
      app.use('/', Router);
    },
    clientLogLevel: 'warning',
    historyApiFallback: {
      rewrites: [
        { from: /.*/, to: path.posix.join(config.dev.assetsPublicPath, 'index.html') },
      ],
    },
    hot: true,
    contentBase: false, // since we use CopyWebpackPlugin.
    compress: true,
    host: HOST || config.dev.host,
    port: PORT || config.dev.port,
    open: config.dev.autoOpenBrowser,
    overlay: config.dev.errorOverlay
      ? { warnings: false, errors: true }
      : false,
    publicPath: config.dev.assetsPublicPath,
    proxy: config.dev.proxyTable,
    quiet: true, // necessary for FriendlyErrorsPlugin
    watchOptions: {
      poll: config.dev.poll,
    }
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': require('../config/dev.env')
    }),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NamedModulesPlugin(), // HMR shows correct file names in console on update.
    new webpack.NoEmitOnErrorsPlugin(),
    // https://github.com/ampedandwired/html-webpack-plugin
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: 'index.html',
      inject: true
    }),
    // copy custom static assets
    new CopyWebpackPlugin([
      {
        from: path.resolve(__dirname, '../static'),
        to: config.dev.assetsSubDirectory,
        ignore: ['.*']
      }
    ])
  ]
})

module.exports = new Promise((resolve, reject) => {
  portfinder.basePort = process.env.PORT || config.dev.port
  portfinder.getPort((err, port) => {
    if (err) {
      reject(err)
    } else {
      // publish the new Port, necessary for e2e tests
      process.env.PORT = port
      // add port to devServer config
      devWebpackConfig.devServer.port = port

      // Add FriendlyErrorsPlugin
      devWebpackConfig.plugins.push(new FriendlyErrorsPlugin({
        compilationSuccessInfo: {
          messages: [`Your application is running here: http://${devWebpackConfig.devServer.host}:${port}`],
        },
        onErrors: config.dev.notifyOnErrors
        ? utils.createNotifierCallback()
        : undefined
      }))

      resolve(devWebpackConfig)
    }
  })
})
