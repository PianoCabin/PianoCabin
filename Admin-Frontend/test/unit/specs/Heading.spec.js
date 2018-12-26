import Vue from 'vue'
import Heading from '../../../src/components/Heading/Heading'

describe('Heading', () => {
  it('should render correct contents', () => {
    const Constructor = Vue.extend(Heading)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('.head-title').textContent).to.equal('琴屋管理员');
    let button_span = vm.$el.querySelectorAll('button[type=button] span')
    expect(button_span[2].textContent).to.be.equal('头像');
    expect(button_span[1].textContent).to.be.equal('账号');
    expect(button_span[0].textContent).to.be.equal('登出');
    for (let button of vm.$el.querySelectorAll('button[type=button]')) {
      expect(typeof button.click).to.be.equal('function');
    }
  })
})
