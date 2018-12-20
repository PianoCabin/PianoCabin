import Vue from 'vue'
import Heading from '../../../src/components/Heading/Heading'

describe('Heading', () => {
  it('should render correct contents', () => {
    const Constructor = Vue.extend(Heading)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('.head-title').textContent)
      .to.equal('琴屋管理员')
  })
})
