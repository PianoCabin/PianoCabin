import App from '../../../src/module/user/App'
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueResource from 'vue-resource'
var expect = require('chai').expect;

/* eslint-disable no-new */

Vue.use(VueResource)
Vue.use(ElementUI)

window.test = true;

describe('用户管理界面', () => {
  const vm = new Vue(App).$mount()

  it('检查内容为空时页面元素', () => {
    expect(vm.$el.querySelectorAll(".side-bar").length > 0).to.be.equal(true);
    expect(vm.$el.querySelectorAll(".search-item").length > 0).to.be.equal(true);
    expect(vm.$el.querySelectorAll(".filter").length > 0).to.be.equal(true);
    expect(vm.$el.querySelectorAll(".info").length > 0).to.be.equal(true);
    expect(vm.$el.querySelectorAll(".fl").length > 0).to.be.equal(true);
    expect(vm.$el.querySelectorAll(".line").length > 0).to.be.equal(true);
    expect(vm.$el.querySelectorAll(".el-table__empty-text").length === 1).to.be.equal(true);
    expect(vm.$el.querySelector(".filter button").disabled).to.be.equal(true);
    expect(vm.$el.querySelector(".el-menu-item.menu-item.is-active span").textContent).to.be.equal("用户管理");
  });
})
