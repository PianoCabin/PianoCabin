import App from '../../../src/module/login/App'
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

describe('登录界面', () => {
  const vm = new Vue(App).$mount()
  it('检查页面元素', () => {

    expect(vm.$el.querySelector("h1").textContent).to.be.equal('登录');
    expect(vm.$el.querySelectorAll('.login-item')[1].textContent).to.be.equal('密码');
    expect(vm.$el.querySelectorAll('.login-item')[0].textContent).to.be.equal('用户名');
    expect(vm.$el.querySelector(".login-button").textContent).to.be.equal('登录');
    expect(typeof vm.$el.querySelector(".login-button").click).to.be.equal('function');
  })
  it('检查用户名、密码数据绑定', () => {
    let test_info = { "username": "mocha_test", "password": "test" }
    vm.login_info = test_info;
    Vue.nextTick(() => {
      Object.keys(test_info).forEach(function (key) {
        expect(vm.$el.querySelector("label[for='" + key + "']+div>div>input.el-input__inner").value).to.be.equal(test_info[key])
      })
    })
  })


})
