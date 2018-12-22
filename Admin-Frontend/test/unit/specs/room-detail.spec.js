import App from '../../../src/module/room-detail/App'
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

describe('琴房详情界面', () => {
    const vm = new Vue(App).$mount()
    it('检查页面元素', () => {

        expect(vm.$el.querySelectorAll(".side-bar").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".heading").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".el-menu").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".edit-card.below").length > 0).to.be.equal(true);
        expect(vm.$el.querySelectorAll(".edit-card").length > 1).to.be.equal(true);

        expect(vm.$el.querySelectorAll(".save-button").length > 0).to.be.equal(true);
        expect(typeof vm.$el.querySelector(".save-button").click).to.be.equal('function');
        expect(vm.$el.querySelectorAll(".return-button").length > 0).to.be.equal(true);
        expect(typeof vm.$el.querySelector(".return-button").click).to.be.equal('function');
        expect(vm.$el.querySelectorAll(".el-dialog").length > 0).to.be.equal(true)
    })
    it('检查琴房信息显示', done => {
        let test_info = { brand: "星海立时钢琴", room_num: "F2-201", piano_type: "钢琴房", price_0: 5, price_1: 10, price_2: 15, usable: "下线", art_ensemble: "非艺术团" };
        vm.room_info = test_info;
        Vue.nextTick(() => {
            expect(vm.$el.querySelector("h1").textContent).to.be.equal(test_info['brand']);
            expect(vm.$el.querySelector("h2").textContent).to.be.equal(test_info['room_num']);
            Object.keys(test_info).forEach(function (key) {
                // console.log(key)
                if (vm.$el.querySelector(".el-form-item.is-required > label[for='" + key + "']+div>div>input.el-input__inner"))
                    expect(vm.$el.querySelector(".el-form-item.is-required > label[for='" + key + "']+div>div>input.el-input__inner").value).to.be.equal(test_info[key].toString())
                else if (vm.$el.querySelector(".el-form-item.is-required > label[for='" + key + "']+div>div>div>input.el-input__inner"))
                    expect(vm.$el.querySelector(".el-form-item.is-required > label[for='" + key + "']+div>div>div>input.el-input__inner").value).to.be.equal(test_info[key].toString())

            });
            done()
        })
    })


})
