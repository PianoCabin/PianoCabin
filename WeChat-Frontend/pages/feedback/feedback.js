// pages/feedback/feedback.js
var util = require("../../utils/util.js")


const app = getApp()

Page({

    /**
     * 页面的初始数据
     */
    data: {
        title: "",
        content: "",
        animation_data: null,
        msg_view: false,
        checked: "false"
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
    },
    commit: function (event) {
        app.feedback({'feedback_title': this.data.title, "feedback_content": this.data.content}, (res) => {
            wx.switchTab({
                url: '/pages/userpage/userpage',
            })
        })
    },
    titleInputConfirm(event) {
        this.setData({title: event.detail.value});
        this.checkMsg()
    },
    contentInputConfirm(event) {
        this.setData({content: event.detail.value});
        this.checkMsg()
    },
    showmsgView() {
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
        this.setData({msg_view: true});
    },
    hidemsgView() {
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
                msg_view: false
            })
        }.bind(this), 100)
    },
    checkMsg() {
        if (this.data.title != "" && this.data.content != "") {
            this.setData({checked: ""})
        } else {
            this.setData({checked: "false"})
        }
    }
})