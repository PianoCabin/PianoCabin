import App from '../../../src/module/feedback-detail/App'
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

describe('反馈详情界面', () => {
    const vm = new Vue(App).$mount()

    it('检查页面元素', () => {
        expect(vm.$el.querySelectorAll(".side-bar").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".heading").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".el-menu").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".feedback-card").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".return-button").length > 0).to.be.equal(true);
        expect(typeof vm.$el.querySelector(".return-button").click).to.be.equal('function');
    })
    it('检查反馈信息显示', () => {
        let test_detail = { user_id: "qwer", feedback_time: 1544369401, feedback_content: "test_content", feedback_title: "test_title" };
        vm.feedback_detail = test_detail;
        Vue.nextTick(() => {
            expect(vm.$el.querySelector('.title>h1').textContent).to.be.equal(test_detail["feedback_title"])
            expect(vm.$el.querySelector('.feedback-content').textContent).to.be.equal(test_detail["feedback_content"])
            expect(vm.$el.querySelector('.publisher').textContent).to.be.equal("发布人：" + test_detail["user_id"])
            expect(vm.$el.querySelector('.publish-time').textContent).to.be.equal("发布时间：" + new Date(test_detail["feedback_time"] * 1000).toLocaleString())
        })
    })
})
