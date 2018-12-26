// pages/help/help.js
Page({

    /**
     * 页面的初始数据
     */
    data: {},
    toUserPage(event) {
        wx.switchTab({
            url: '/pages/userpage/userpage',
        })
    },
    onPullDownRefresh() {
        wx.stopPullDownRefresh();
    }
})