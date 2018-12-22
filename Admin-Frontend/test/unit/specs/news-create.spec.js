import App from '../../../src/module/news-create/App'
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

describe('信息详情界面', () => {
    const vm = new Vue(App).$mount()
    it('检查页面元素', () => {
        expect(vm.$el.querySelectorAll(".side-bar").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".heading").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".el-menu").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".save-button").length > 0).to.be.equal(true);
        expect(typeof vm.$el.querySelector(".save-button").click).to.be.equal('function');
    })

    it('检查信息数据绑定', done=> {
        let test_info = { news_title: "title", news_content: "content" }
        vm.news_info = test_info;
        Vue.nextTick(() => {
            expect(vm.$el.querySelector('input').value).to.be.equal(test_info["news_title"])
            expect(vm.$el.querySelector('textarea').value).to.be.equal(test_info["news_content"])
            done()
        })
    })
})
