//index.js
//获取应用实例
var util = require("../../utils/util.js")


const app = getApp()

let page = Page({
    data: {
        list_type: null,                                         //当前显示的列表的类型（钢琴、小琴房或电钢琴）
        cur_date: "",                                            //当前选择的日期
        cur_date_show: "",
        search_start: null,                                      //按时间查找的开始时间
        search_end: null,                                        //按时间查找的结束时间
        selected_room: "",                                     //选中的房间在列表中的id
        search_room_num: "",                                     //查询琴的种类
        show_order_info: false,                                  //是否显示订单弹窗
        order_info: {},                                          //订单的详细内容
        animation_data: null,                                    //动画接口
        animation_time: 100,                                     //动画执行时间
        room_list: [],                                          //显示的琴房的信息列表
        starttime_list: [],                                      //订单窗口，开始时间的picker的range
        endtime_list: [],                                       //订单窗口，结束时间的picker的range
        free_time_color: "#AAAAAA",                              //未被占用的时间的展示条颜色
        occupied_time_color: "#8E2782",                         //已被占用的时间的展示条颜色
        open_time: [12, 0],                                       //琴房开放开始时间【小时，分钟】
        close_time: [22, 30],                                     //琴房开放结束时间【小时，分钟】
        min_order: 60 * 60 * 1000,                                   //最短预约时间
        min_interval: 10 * 60 * 1000,                                //开始时间最短间隔
        search_start_list: [],                                   //搜索开始时间列表
        search_end_list: [],                                     //搜索结束时间列表
        completeable: true,                                      //订单是否可支付
        type_list: ["钢琴房", "小琴房", "电钢琴"],                   //琴屋种类列表
        type_id: 0,
        time: 0,                                                 //移动计时
        touch_dot: 0,                                            //开始点击屏幕的横坐标
        interval: null,                                          //计时器
        timeout: false,                                          //是否处于手势停用期
        hand_dir: 0,                                             //手势方向
        brand_list:[],
        brand_index:0,
        default_brand_input_content:"点击选择品牌"
    },

    //初始化页面，默认显示钢琴页面
    onReady: function () {
        this.setData({
            piano_id: "select_type",
            room_id: "",
            keyboard_id: "",
            cur_date: new Date().toLocaleDateString(),
            list_type: this.data.type_list[0],
            cur_date_show: util.datetimeShowString(new Date())
        });
        this.getRoomList();
        this.initSearchPage();
    },
    onPullDownRefresh() {
        console.log("pulldown");
        this.resetSearch()
        this.getRoomList();
    },
    onShow: function () {
        this.initSearchPage();
        this.getRoomList();
    },


    //显示钢琴列表
    pianoList: function (event) {
        let type_id = event.currentTarget.id;
        this.setData({
            piano_id: "select_type",
            room_id: "",
            keyboard_id: "",
            list_type: this.data.type_list[type_id],
            room_list: [],
            type_id: type_id
        })
        this.getRoomList();

    },
    //预约日期向前推一天
    dayBefore: function (event) {
        let cur = new Date(this.data.cur_date);
        let new_date = new Date(cur.getTime() - 1000 * 60 * 60 * 24);
        let today = new Date()
        today.setHours(0, 0, 0, 0);
        if (new_date >= today) {
            this.setData({cur_date: new_date.toLocaleDateString(), cur_date_show: util.datetimeShowString(new_date)});
            this.getRoomList(false);
        }
    },

    //预约日期向后推一天
    dayAfter: function (event) {
        let cur = new Date(this.data.cur_date);
        let new_date = new Date(cur.getTime() + 1000 * 60 * 60 * 24);
        let latest = new Date()
        latest.setHours(0, 0, 0, 0);
        let seven_day = latest.getTime() + 7 * 24 * 60 * 60 * 1000;
        if (seven_day > new_date) {
            this.setData({cur_date: new_date.toLocaleDateString(), cur_date_show: util.datetimeShowString(new_date)});
            this.getRoomList(false);
        }
    },

    //点击选中某个房间后，弹出订单框
    selectRoom: function (event) {

        //设置订单的房间信息为选中的房间，并且记录订单的日期为当前选择的日期

        let room_info = this.data.room_list[event.currentTarget.id];
        room_info["date"] = this.data.cur_date;
        this.setData({order_info: room_info});

        //初始化订单框中的数据，包括时间picker和价格量
        this.initOrderPage();

        //调用订单框弹出动画
        this.orderInfoAnimation();

        ////计算可选的预约开始时间列表

        let start_list = [];
        let start = util.timeStringToTimestamp(this.data.cur_date, this.data.open_time[0].toString() + ':' + this.data.open_time[1].toString())
        let end = util.timeStringToTimestamp(this.data.cur_date, this.data.close_time[0].toString() + ':' + this.data.close_time[1].toString())

        let orders = room_info["occupied_time"];
        let now = new Date();
        let mim = parseInt(now.getMinutes() / 10) + 1;
        now.setMinutes(mim * 10, 0, 0);
        now = now.getTime();

        for (let i = 0; i < orders.length; i++) {
            //查找每一段时长大于min_order的空闲时间
            if (orders[i][0] - start >= this.data.min_order && orders[i][0] > now) {
                let ss = orders[i][0];
                start = Math.max(start, now);
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
        let ss = Math.max(util.timeStringToTimestamp(this.data.cur_date, this.data.open_time[0].toString() + ':' + this.data.open_time[1].toString()), now);
        if (orders.length > 0)
            ss = Math.max(orders[orders.length - 1][1], now);

        while (end - ss >= this.data.min_order && ss >= now) {
            let tt = new Date(ss);
            let startable = util.timestampToTimeString(tt);
            start_list.push(startable);
            ss = ss + this.data.min_interval;
        }

        this.setData({starttime_list: start_list});
        this.setData({selected_room: event.currentTarget.id})

    },
    search: function (event) {

        this.hideSearchPage();
        this.getRoomList(false);
    },


    //订单框弹出动画
    orderInfoAnimation() {
        var that = this;
        var animation = wx.createAnimation({
            duration: this.data.animation_time,
            timingFunction: 'linear'
        })
        that.animation = animation
        animation.translateY(350).step()
        that.setData({
            animation_data: animation.export(),
        })
        setTimeout(function () {
            animation.translateY(0).step()
            that.setData({
                animation_data: animation.export()
            })
        }, 100)
        that.setData({show_order_info: true});
    },

    //订单框收回动画
    hideOrderInfo: function (e) {
        var that = this;
        var animation = wx.createAnimation({
            duration: this.data.animation_time,
            timingFunction: 'linear',
        })
        that.animation = animation
        animation.translateY(350).step()
        that.setData({
            animation_data: animation.export()
        })
        setTimeout(function () {
            animation.translateY(0).step()
            that.setData({
                animation_data: animation.export(),
            })
        }, 200)
        setTimeout(function () {
            animation.translateY(0).step()
            that.setData({
                animation_data: animation.export(),
                show_order_info: false
            })
        }, 200)
    },

    //搜索框弹出动画
    searchPageAnimation() {
        var that = this;
        var animation = wx.createAnimation({
            duration: this.data.animation_time,
            timingFunction: 'linear'
        })
        that.animation = animation
        animation.translateY(350).step()
        that.setData({
            animation_data: animation.export(),
        })
        setTimeout(function () {
            animation.translateY(0).step()
            that.setData({
                animation_data: animation.export()
            })
        }, 100)
        that.setData({show_search_page: true});
    },

    //搜索框收回动画
    hideSearchPage: function (e) {
        var that = this;
        var animation = wx.createAnimation({
            duration: this.data.animation_time,
            timingFunction: 'linear',
        })
        that.animation = animation
        animation.translateY(350).step()
        that.setData({
            animation_data: animation.export()
        })
        setTimeout(function () {
            animation.translateY(0).step()
            that.setData({
                animation_data: animation.export(),
            })
        }, 200)
        setTimeout(function () {
            animation.translateY(0).step()
            that.setData({
                animation_data: animation.export(),
                show_search_page: false
            })
        }, 200)
    },

    //向服务器请求筛选过的琴房列表
    getRoomList(update_search_list = true) {
        let data = this.getListFilter();
        if (data["type"] != null)
        {
          if(update_search_list)
            app.getRoomList(data, this.showRoomList);
          else
            app.getRoomList(data, this.showRoomList_2);

        }
    },
    showRoomList(res) {
        let list = res.data["data"]["room_list"];
        this.updateList(list);
        wx.stopPullDownRefresh()
    },
    showRoomList_2(res){
      let list = res.data["data"]["room_list"];
      this.updateList(list,false);
      wx.stopPullDownRefresh()
    },
    //获取琴房筛选条件
    getListFilter() {
        let data = {};
        data["type"] = this.data.list_type;
        let transer = (new Date(this.data.cur_date));
        transer.setHours(12, 0, 0, 0);
        data["date"] = transer.getTime() / 1000;
        if (this.data.search_start != null)
            data["start_time"] = util.timeStringToTimestamp(this.data.cur_date, this.data.search_start) / 1000;
        if (this.data.search_end != null)
            data["end_time"] = util.timeStringToTimestamp(this.data.cur_date, this.data.search_end) / 1000;
        if (this.data.search_room_num != this.data.default_brand_input_content)
            data["brand"] = this.data.search_room_num;
        return data;
    },

    //根据传入的房间列表（服务器端）数据，更新琴房列表数据
    updateList(data_list,update_search_list = true) {
        let new_brand = []
        let new_list = []
        let start_time = util.timeStringToTimestamp(this.data.cur_date, this.data.open_time[0].toString() + ':' + '00');
        let end_time = util.timeStringToTimestamp(this.data.cur_date, (this.data.close_time[0] + (this.data.close_time[1] > 0)).toString() + ':' + "00");

        //每个房间更新数据
        for (let i = 0; i < data_list.length; i++) {
          if ((new_brand.indexOf(data_list[i]["brand"]) == -1))
            new_brand.push(data_list[i]["brand"]);
            let element = {}
            element["name"] = data_list[i]["brand"];
            element["room_num"] = data_list[i]["room_num"];
            element["price"] = data_list[i]["unit_price"];
            element["hours"] = [];

            for (let i = this.data.open_time[0]; i < this.data.close_time[0] + 1; i++) {
                if (i == this.data.close_time[0] && this.data.close_time[1] > 0) {
                    element["hours"].push(i);
                    element["hours"].push(i + 1);
                    element["end_hour"] = i + 1;
                } else if (i == this.data.close_time[0] && this.data.close_time[1] == 0) {
                    element["end_hour"] = i;
                    element["hours"].push(i);

                } else
                    element["hours"].push(i);
            }
            element["label_offset"] = ((95 / element["hours"].length) / 2);
            element["time_bar_len"] = 95 - 2 * element["label_offset"];

            //将后端的10位时间戳转为js的13位时间戳
            element["occupied_time"] = data_list[i]["occupied_time"];
            for (let i = 0; i < element["occupied_time"].length; i++) {
                element["occupied_time"][i][0] *= 1000;
                element["occupied_time"][i][1] *= 1000;
                if (i > 0) {
                    if (element["occupied_time"][i][0] == element["occupied_time"][i - 1][0] && element["occupied_time"][i][1] == element["occupied_time"][i - 1][1]) {
                        element["occupied_time"].splice(i, 1);
                        i = i - 1;
                    }
                }
            }

            //根据占用时间，计算整个预约开放时间内时间的空闲占用情况
            let hour_list = [];
            let time_left = start_time;
            for (let j = 0; j < element["occupied_time"].length; j++) {
                let order1 = {};

                order1["width"] = ((element["occupied_time"][j][0] - time_left) / (end_time - start_time) * 100);
                order1["color"] = this.data.free_time_color;
                hour_list.push(order1);

                let order2 = {};
                order2["width"] = ((element["occupied_time"][j][1] - element["occupied_time"][j][0]) / (end_time - start_time) * 100);
                order2["color"] = this.data.occupied_time_color;
                hour_list.push(order2);

                time_left = element["occupied_time"][j][1];

                if (j == element["occupied_time"].length - 1) {
                    if (element["occupied_time"][j][1] < end_time) {
                        let order3 = {};
                        order3["width"] = ((end_time - element["occupied_time"][j][1]) / (end_time - start_time) * 100);
                        order3["color"] = this.data.free_time_color;
                        hour_list.push(order3);
                    }
                }
            }
            if (element["occupied_time"].length == 0) {
                let order4 = {};
                order4["width"] = 100;
                order4["color"] = this.data.free_time_color;
                hour_list.push(order4);
            }

            element["time"] = hour_list;
            new_list.push(element);
        }
      this.setData({ room_list: new_list});
      if(update_search_list)
        this.setData({brand_list:new_brand});
        return new_list;
    },

    //根据选择的开始时间，计算可能的结束时间
    setOrderStart(event) {
        let info = this.data.order_info;
        let end_list = [];
        let index = event.detail["value"];
        let room_info = this.data.room_list[this.data.selected_room];

        let list = this.data.starttime_list[index].split(":");
        let start = new Date(util.timeStringToTimestamp(this.data.cur_date, this.data.starttime_list[index]));
        let max_end = util.timeStringToTimestamp(this.data.cur_date, this.data.open_time[0].toString() + ':' + this.data.open_time[1].toString());


        for (let i = 0; i < room_info["occupied_time"].length; i++) {
            if (start <= room_info["occupied_time"][i][0]) {
                max_end = room_info["occupied_time"][i][0];

                break;
            }
            if (i == room_info["occupied_time"].length - 1) {
                max_end = util.timeStringToTimestamp(this.data.cur_date, this.data.close_time[0].toString() + ':' + this.data.close_time[1].toString());
            }
        }

        if (room_info["occupied_time"].length == 0) {
            max_end = util.timeStringToTimestamp(this.data.cur_date, this.data.close_time[0].toString() + ':' + this.data.close_time[1].toString());
        }


        start = start.getTime() + this.data.min_order;

        while (start <= max_end) {
            end_list.push(util.timestampToTimeString(start));
            start = start + this.data.min_interval;
        }
        info["order_start"] = this.data.starttime_list[index];
        info["order_end"] = "结束";
        info["price"] = "";
        this.setData({endtime_list: end_list, order_info: info, completeable: true});
    },

    //根据开始和结束时间更新显示与订单价格
    updateOrder(event) {
        let index = event.detail["value"];
        let info = this.data.order_info;
        let unit_price = this.data.room_list[this.data.selected_room]["price"];
        info["order_end"] = this.data.endtime_list[index];

        let order_start = util.timeStringToTimestamp(this.data.cur_date, info["order_start"]);
        let order_end = util.timeStringToTimestamp(this.data.cur_date, info["order_end"]);
        let hour_num = parseInt((order_end - order_start) / (60 * 60 * 1000)) + ((order_end - order_start) % (60 * 60 * 1000) > 0);
        info["price"] = unit_price * hour_num;
        this.setData({order_info: info, completeable: ""});
    },

    //初始化订单框中的数据
    initOrderPage() {
        let info = this.data.order_info;
        info["order_start"] = "开始";
        info["price"] = "";
        info["order_end"] = "结束";
        this.setData({
            starttime_list: [],
            endtime_list: [],
            order_info: info
        })
    },
    showSearchPage() {
        this.initSearchPage();
        this.searchPageAnimation();
    },

    initSearchPage() {
        let ss_list = [];
        let search_start_stamp = util.timeStringToTimestamp(this.data.cur_date, this.data.open_time[0].toString() + ":" + this.data.open_time[1].toString());
        let search_end_stamp = util.timeStringToTimestamp(this.data.cur_date, this.data.close_time[0].toString() + ":" + this.data.close_time[1].toString());
        for (let i = search_start_stamp + this.data.min_order; i < search_end_stamp; i += this.data.min_interval) {
            ss_list.push(util.timestampToTimeString(i));
        }
        this.setData({
            search_start_list: ss_list,
            search_end_list: ss_list,
            search_start: util.formatNumber(this.data.open_time[0]) + ':' + util.formatNumber(this.data.open_time[1]),
            search_end: util.formatNumber(this.data.close_time[0]) + ':' + util.formatNumber(this.data.close_time[1]),
            search_room_num: this.data.default_brand_input_content
        });
    },
    setSearchStart(event) {
        this.initSearchPage();
        let index = event.detail["value"];
        let start = util.timeStringToTimestamp(this.data.cur_date, this.data.search_start_list[index]);
        let end = util.timeStringToTimestamp(this.data.cur_date, this.data.close_time[0] + ':' + this.data.close_time[1]);
        let end_list = []
        for (let i = Math.min(start + this.data.min_order, end); i < end + this.data.min_interval; i += this.data.min_interval) {
            end_list.push(util.timestampToTimeString(i));
        }
        this.setData({search_end_list: end_list, search_start: this.data.search_start_list[index]});
    },
    setSearchEnd(event) {
        let index = event.detail["value"];
        let end = this.data.search_end_list[index];
        let end_stamp = util.timeStringToTimestamp(this.data.cur_date, end);
        let start_stamp = util.timeStringToTimestamp(this.data.cur_date, this.data.search_start);
        if (start_stamp > end_stamp)
            start_stamp = end_stamp;
        this.setData({
            search_end: end,
            search_start: util.timestampToTimeString(start_stamp)
        });
    },
    searchInputConfirm(event) {
        this.setData({search_room_num: this.data.brand_list[event.detail.value]});
    },
    checkOrderInfo() {
        if (this.data.order_info["order_start"] != "开始" && this.data.order_info["order_end"] != "结束" && this.data.order_info["price"] != "") {
          let now = (new Date()).getTime();
          let start_time = util.timeStringToTimestamp(this.data.cur_date,this.data.order_info["order_start"]);
          if(start_time<=now){
            util.msgPrompt("请重新选择预约时间",false);
            return false;
          }
            return true;
        }
        return false;
    },
    createOrder() {
        let order = {};
        order["room_num"] = this.data.order_info["room_num"];
        order["start_time"] = parseInt(util.timeStringToTimestamp(this.data.cur_date, this.data.order_info["order_start"]) / 1000);
        order["end_time"] = parseInt(util.timeStringToTimestamp(this.data.cur_date, this.data.order_info["order_end"]) / 1000);
        order["price"] = this.data.order_info["price"];
        return order;
    },
    orderComplete(event) {
        if (this.checkOrderInfo()) {
            let order = this.createOrder();

            this.submitOrder(order);
        } else {
            util.msgPrompt("no complete", false)
        }
    },
    submitOrder(order_data) {
        app.submitOrder(order_data, this.goToOrderInfo);
    },
    goToOrderInfo(res) {
        wx.redirectTo({
            url: '/pages/orderinfo/orderinfo?order_id=' + res.data["data"]["order_id"].toString(),
        })
    },
    resetSearch() {
        this.setData({
            search_start: null,
            search_end: null,
            search_room_num: this.data.default_brand_input_content
        })
    },
    // 触摸开始事件
    touchStart: function (e) {
        if (this.data.timeout)
            return;
        console.log("start touch");
        this.data.touch_dot = e.touches[0].pageX; // 获取触摸时的原点
        // 使用js计时器记录时间
        let _this = this

        this.data.interval = setInterval(function () {
            _this.data.time++;
        }, 100);
    },
    // 触摸移动事件
    touchMove: function (e) {
        if (this.data.timeout)
            return;
        let touchMove = e.touches[0].pageX;
        if (touchMove - this.data.touch_dot <= -100 && this.data.time < 10) {
            console.log('向左滑动');
            this.data.hand_dir = 1;
            this.data.timeout = true;
        }
        // 向右滑动
        if (touchMove - this.data.touch_dot >= 100 && this.data.time < 10) {
            console.log('向右滑动');
            this.data.hand_dir = 2;
            this.data.timeout = true;
        }
    },
    // 触摸结束事件
    touchEnd: function (e) {
        if (this.data.timeout) {
            let _this = this;
            setTimeout(() => {
                _this.data.timeout = false
            }, 500)
            if (this.data.hand_dir == 1)
                this.dayAfter(null);
            else if (this.data.hand_dir == 2)
                this.dayBefore(null);
        }
        console.log("touch end")
        clearInterval(this.data.interval); // 清除setInterval
        this.data.time = 0;
    }
})


module.exports = page;