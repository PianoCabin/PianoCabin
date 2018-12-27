// pages/orderinfo/orderinfo.js

var util = require("../../utils/util.js")

const app = getApp()


const OrderStatus = ["已取消", '未付款', '已付款', '已完成']


Page({

    /**
     * 页面的初始数据
     */
    data: {
        info: {},
        edit: false,
        min_order: 60 * 60 * 1000,
        min_interval: 10 * 60 * 1000,
        starttime_list: [],
        endtime_list: [],
        cur_date: "",
        roominfo: {},
        animation_data: null,
        cancel_view: false,
        open_time: [12, 0],
        close_time: [22, 30],
        nickname: "默认用户",
        saved: true,
        valid: true
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        let order_id = options.order_id;
        this.getOrderInfo(order_id);

        // this.setData({
        //   nickname: app.globalData.user_nickname
        // })
    },
    onShow() {
        // this.setData({
        //   nickname: app.globalData.user_nickname
        // })
    },
    getOrderInfo(order_id) {
        app.getOrderList({order_id: order_id}, this.updateOrderInfo)
    },
    updateOrderInfo(res) {
        let data = res.data["data"]["order_list"][0]
        let info = {};
        info["piano_type"] = data["brand"];
        info["type"] = data["piano_type"]
        info["room_num"] = data["room_num"];
        info["price"] = data["price"];
        info["order_status"] = OrderStatus[data["order_status"]];
        info["order_id"] = data["order_id"];
        info["status"] = data["order_status"];
        info["user_id"] = app.globalData.user_session;
        info["date"] = util.timestampToDateString(data['start_time'] * 1000);
        info["start_time"] = data["start_time"] * 1000;
        info["end_time"] = data["end_time"] * 1000;
        info["order_start"] = util.timestampToTimeString(data['start_time'] * 1000);
        info["order_end"] = util.timestampToTimeString(data['end_time'] * 1000);
        info["user_id"] = data["user_id"];
        info["qrcode"] = data["qrcode"];

        this.setData({
            info: info,
            start_time: util.timestampToTimeString(data["start_time"] * 1000),
            end_time: util.timestampToTimeString(data["end_time"] * 1000),
            cur_date: (new Date(data["start_time"] * 1000)).toLocaleDateString()
        })
        if (data["order_status"] == 1)
            this.getRoomInfo(data["room_num"]);
    },
    getRoomInfo(room_num) {
      let today = new Date(this.data.info["date"])
        today.setHours(12, 0, 0, 0);
        app.getRoomList({
                room_num: room_num,
                date: today.getTime() / 1000,
                type: this.data.info["type"]
            },
            this.setOrderInfo);
    },
    setOrderInfo(res) {
        this.setStartList(res.data["data"]["room_list"][0]);
        this.initEndList(res.data["data"]["room_list"][0]);
        this.setData({
            roominfo: res.data['data']["room_list"][0]
        })
    },
    setStartList(room_info) {
        let transer = new Date(this.data.info["date"])
        transer.setHours(this.data.open_time[0], this.data.open_time[1], 0, 0)
        let start = transer.getTime();
        transer.setHours(this.data.close_time[0], this.data.close_time[1], 0, 0);
        let end = transer.getTime();
        let start_list = [];

        let orders = room_info["occupied_time"];
        console.log("here");
        console.log(orders);

        for (let i = 0; i < orders.length; i++) {
            orders[i][0] *= 1000;
            orders[i][1] *= 1000;
            if (orders[i][0] == this.data.info["start_time"] && orders[i][1] == this.data.info["end_time"]) {
                orders.splice(i, 1);
                i--;
            }
        }


        let now = new Date();
        let mim = parseInt(now.getMinutes() / 10) + 1;
        now.setMinutes(mim * 10, 0, 0);
        now = now.getTime();

        console.log("2");
        console.log(orders)
        console.log(start)
        console.log(now)
        for (let i = 0; i < orders.length; i++) {
          console.log(orders[i][0] - start >= this.data.min_order)
          console.log(orders[i][0] > now)
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
        transer.setHours(this.data.open_time[0], this.data.open_time[1], 0, 0)
        let ss = Math.max(transer.getTime(), now);
        if (orders.length > 0)
            ss = Math.max(orders[orders.length - 1][1], now);

        while (end - ss >= this.data.min_order && ss >= now) {
            let tt = new Date(ss);
            let startable = util.timestampToTimeString(tt);
            start_list.push(startable);
            ss = ss + this.data.min_interval;
        }
        this.setData({starttime_list: start_list, edit: true});
    },
    initEndList(room_info) {
        let end_list = [];
      let transer = new Date(this.data.info["date"])
        transer.setHours(this.data.close_time[0], this.data.close_time[1], 0, 0)
        let start = new Date(this.data.info["start_time"]);
        let max_end = transer.getTime();

        for (let i = 0; i < room_info["occupied_time"].length; i++) {
            if (start <= room_info["occupied_time"][i][0]) {
                max_end = room_info["occupied_time"][i][0];
                break;
            }
            if (i == room_info["occupied_time"].length - 1) {
                transer.setHours(this.data.close_time[0], this.data.close_time[1], 0, 0)
                max_end = transer.getTime();
            }
        }
        start = start.getTime() + this.data.min_order;
        while (start <= max_end) {
            end_list.push(util.timestampToTimeString(start));
            start = start + this.data.min_interval;
        }
        this.setData({endtime_list: end_list});
    },
    setOrderStart(event) {
        let info = this.data.info;
        let end_list = [];
        let index = event.detail["value"];
        let room_info = this.data.roominfo;

        let list = this.data.starttime_list[index].split(":");
      let transer = new Date(this.data.info["date"])
        transer.setHours(this.data.close_time[0], this.data.close_time[1], 0, 0)
        let start = new Date(util.timeStringToTimestamp(this.data.cur_date, this.data.starttime_list[index]));

        let max_end = transer.getTime();

        for (let i = 0; i < room_info["occupied_time"].length; i++) {
            if (start <= room_info["occupied_time"][i][0]) {
                max_end = room_info["occupied_time"][i][0];
                break;
            }
            if (i == room_info["occupied_time"].length - 1) {
                transer.setHours(this.data.close_time[0], this.data.close_time[1], 0, 0)
                max_end = transer.getTime();
            }
        }

        start = start.getTime() + this.data.min_order;
        while (start <= max_end) {
            end_list.push(util.timestampToTimeString(start));
            start = start + this.data.min_interval;
        }

        info["order_start"] = this.data.starttime_list[index];
        start = util.timeStringToTimestamp(this.data.cur_date, info["order_start"]);
        if (info["end_time"] - start < this.data.min_order) {
            info["order_end"] = "结束";
            info["price"] = "";
            this.setData({
                endtime_list: end_list,
                info: info,
                start_time: info["order_start"],
                end_time: info['order_end'],
                saved: false,
                valid: false
            });
        } else {
            let end = util.timeStringToTimestamp(this.data.cur_date, info["order_end"]);
            let hours = parseInt((end - start) / (60 * 60 * 1000)) + ((end - start) % (60 * 60 * 1000) > 0);
            let newprice = hours * this.data.roominfo["unit_price"];
            info["price"] = newprice;
            this.setData({
                info: info,
                saved: false,
                start_time: info["order_start"], end_time: info['order_end'],
                valid: true
            })
        }
    },
    setOrderEnd(event) {
        let index = event.detail["value"];
        let start = util.timeStringToTimestamp(this.data.cur_date, this.data.start_time);
        let end = util.timeStringToTimestamp(this.data.cur_date, this.data.endtime_list[index]);
        let hours = parseInt((end - start) / (60 * 60 * 1000)) + ((end - start) % (60 * 60 * 1000) > 0);
        let newprice = hours * this.data.roominfo["unit_price"];
        let info = this.data.info;
        info["price"] = newprice;
        info["order_end"] = this.data.endtime_list[index];
        this.setData({
            end_time: info["order_end"],
            info: info,
            saved: false,
            valid: true
        })
    },
    toOrderPage() {
        wx.redirectTo({
            url: '/pages/orderpage/orderpage',
        })
    },
    changeOrder() {
        let info = this.getInfoObject();

        app.changeOrder(info, res => {
            this.onLoad({order_id: info["order_id"]});
            this.setData({saved: true});
        });

    },
    cancelOrder() {
        app.cancelOrder({order_id: this.data.info["order_id"]}, res => {

            wx.redirectTo({
                url: '/pages/orderpage/orderpage',
            })
        })
    },
    checkCancelOrder() {
        this.showCancelView();
    },
    getInfoObject() {
        let info = {};
      let transer = new Date(this.data.info["date"]);
        transer.setHours(12, 0, 0, 0);
        info["room_num"] = this.data.info["room_num"];
        info["start_time"] = util.timeStringToTimestamp(this.data.info["date"], this.data.info["order_start"]) / 1000;
        info["end_time"] = util.timeStringToTimestamp(this.data.info["date"], this.data.info["order_end"]) / 1000;
        info["price"] = this.data.info["price"];
        info["order_id"] = this.data.info["order_id"];
        info["date"] = util.timeStringToTimestamp(this.data.info["date"], "12:00") / 1000;

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
        this.setData({cancel_view: true});
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
    payOrder() {
        app.getPayMsg({"order_id": this.data.info["order_id"]}, (res) => {

            app.payForOrder(res.data["data"]['timeStamp'], res.data["data"]['nonceStr'], res.data["data"]['package'], res.data["data"]['paySign']);
        });
    }
})