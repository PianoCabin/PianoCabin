import App from '../../../src/module/order/App'
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueResource from 'vue-resource'
var expect = require('chai').expect;
import { mount } from 'avoriaz';

/* eslint-disable no-new */

Vue.use(VueResource)
Vue.use(ElementUI)

window.test = true;

describe('订单列表界面', () => {
    const vm = new Vue(App).$mount()
    it('检查页面元素', () => {
        expect(vm.$el.querySelectorAll(".side-bar").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".heading").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".el-menu").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".filter").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".content.select-panel").length > 0).to.be.equal(true);
    })
    it('检查搜索框数据绑定', done => {
        let test_filter = { order_id: 'asdfg', room_num: 'F2-201', user_id: 'abc' };
        vm.filter_info = test_filter;
        Vue.nextTick(() => {
            expect(vm.$el.querySelectorAll(".search-item.fl")[0].childNodes[2].childNodes[1].value).to.be.equal(test_filter['order_id'])
            expect(vm.$el.querySelectorAll(".search-item.fl")[1].childNodes[2].childNodes[1].value).to.be.equal(test_filter['room_num'])
            expect(vm.$el.querySelectorAll(".search-item.fl")[2].childNodes[2].childNodes[1].value).to.be.equal(test_filter['user_id'])
            done()
        })
    })
    it('检查搜索日期数据绑定', done => {
        let test_range = [100, 1544358383184];
        vm.date_range = test_range;
        Vue.nextTick(() => {
            let year = new Date(test_range[0]).getFullYear().toString()
            let month = (new Date(test_range[0]).getMonth() + 1).toString() < 10 ? '0' + (new Date(test_range[0]).getMonth() + 1).toString() : (new Date(test_range[0]).getMonth() + 1).toString()
            let date = new Date(test_range[0]).getDate().toString() < 10 ? '0' + new Date(test_range[0]).getDate().toString() : new Date(test_range[0]).getDate().toString()
            let start = year + '-' + month + '-' + date;
            year = new Date(test_range[1]).getFullYear().toString()
            date = new Date(test_range[1]).getDate().toString() < 10 ? '0' + new Date(test_range[1]).getDate().toString() : new Date(test_range[1]).getDate().toString()
            month = (new Date(test_range[1]).getMonth() + 1).toString() < 10 ? '0' + (new Date(test_range[1]).getMonth() + 1).toString() : (new Date(test_range[1]).getMonth() + 1).toString()
            date = new Date(test_range[1]).getDate().toString() < 10 ? '0' + new Date(test_range[1]).getDate().toString() : new Date(test_range[1]).getDate().toString()
            let end = year + '-' + month + '-' + date;
            expect(vm.$el.querySelectorAll(".search-item.fl")[3].childNodes[2].childNodes[1].value).to.be.equal(start);
            expect(vm.$el.querySelectorAll(".search-item.fl")[3].childNodes[2].childNodes[3].value).to.be.equal(end);
            done()
        })
    })
    it('检查订单列表显示', done => {
        vm.order_list = [{ 'brand': "星海立时钢琴", "room_num": "F2-201", "user_id": "abc", "order_id": "sdf", "start_time": 100, "end_time": 200, "create_time": 10, "order_status": 1, "order_price": 15 }]
        vm.total_len = 1;
        vm.page_end = 1;
        Vue.nextTick(() => {
            expect(vm.$el.querySelectorAll('.order-card').length === 1).to.be.equal(true)
            done()
        })
    })
})
