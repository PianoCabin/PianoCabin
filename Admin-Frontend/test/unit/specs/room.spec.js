import App from '../../../src/module/room/App'
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

describe('琴房列表界面', () => {
    const vm = new Vue(App).$mount()
    it('检查页面元素', () => {
        expect(vm.$el.querySelectorAll(".side-bar").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".heading").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".el-menu").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".fab").length > 0).to.be.equal(true);
        expect(typeof vm.$el.querySelector(".fab").click).to.be.equal('function');
    })
    it('检查琴房种类列表数据绑定', () => {
        vm.room_list = { "钢琴房": {}, "电钢琴": {}, "小琴房": {}, "test": {} };
        Vue.nextTick(() => {
            expect(vm.$el.querySelectorAll(".el-submenu").length === 4).to.be.equal(true);
        })
    })
    it('检查房间列表数据绑定', () => {
        vm.selected_list = [{ "room_num": "F2-201" }, { "room_num": "F2-202" }, { "room_num": "F2-203" }];
        Vue.nextTick(() => {
            expect(vm.$el.querySelectorAll(".room").length === 3).to.be.equal(true);
            expect(typeof vm.$el.querySelector('.room').click).to.be.equal('function')
        })
    })
})
