import App from '../../../src/module/news/App'
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

describe('信息列表界面', () => {
    const vm = new Vue(App).$mount()
    it('检查页面元素', () => {

        expect(vm.$el.querySelectorAll(".side-bar").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".heading").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".el-menu").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".content.select-panel").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".fab").length > 0).to.be.equal(true);
        expect(typeof vm.$el.querySelector(".fab").click).to.be.equal('function');
        expect(vm.$el.querySelectorAll(".pagination-div").length > 0).to.be.equal(true)
    })
    it('检查信息列表显示', done => {
        vm.news_list = [{ 'news_title': "test", 'publish_time': 100, "news_id": 1 }]
        vm.page_end = 1;
        vm.total_len = 1;
        Vue.nextTick(() => {
            expect(vm.$el.querySelectorAll('.news-card').length).to.be.equal(1)
            expect(typeof vm.$el.querySelectorAll('.news-card')[0].click).to.be.equal('function')
            done()
        })
    })
})
