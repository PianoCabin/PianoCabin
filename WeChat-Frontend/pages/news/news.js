var util = require("../../utils/util.js")


const app = getApp()


// pages/news/news.js
Page({
    data: {
        news_list: [],
        animation_data: null,
        news_view: false,
        news_detail: {
            "news_title": "",
            "news_content": "",
            "publish_time": ""
        }
    },
    onLoad: function (options) {
        this.getNewsList()
    },
    onPullDownRefresh() {
        this.getNewsList();
    },
    getNewsList() {
        app.getNewsList({}, this.updateNewsList)
    },
    updateNewsList(res) {
        let res_list = res.data["data"]["news_list"];
        res_list.sort((a, b) => {
            return a["publish_time"] < b["publish_time"]
        })
        for (let i = 0; i < res_list.length; i++) {
            res_list[i]["publish_time"] = util.timestampToDateTimeString(res_list[i]["publish_time"] * 1000)
            res_list[i]["index"] = i;
        }
        this.setData({news_list: res_list})
        wx.stopPullDownRefresh();
    },
    newsDetail(event) {
        let news_id = event.currentTarget.id
        // console.log(this.data.news_list[news_id])
        this.setData({news_detail: this.data.news_list[news_id]})
        console.log(this.data.news_detail)
        this.shownewsView();
    },
    shownewsView() {
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
        this.setData({news_view: true});
    },
    hidenewsView() {
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
                news_view: false
            })
        }.bind(this), 100)
    },
    toUserPage() {
        wx.switchTab({
            url: '/pages/userpage/userpage',
        })
    }
})