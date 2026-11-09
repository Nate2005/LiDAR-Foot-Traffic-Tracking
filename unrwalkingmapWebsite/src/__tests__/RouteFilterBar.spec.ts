import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import RouteFilterBar from '../components/RouteFilterBar.vue'

function buttons(wrapper: ReturnType<typeof mount>) {
  return wrapper.findAll('button')
}

describe('RouteFilterBar', () => {
  it('defaults to walking with ADA off', () => {
    const wrapper = mount(RouteFilterBar)
    const [walking, bike, ada] = buttons(wrapper)
    expect(walking!.attributes('aria-pressed')).toBe('true')
    expect(bike!.attributes('aria-pressed')).toBe('false')
    expect(ada!.attributes('aria-pressed')).toBe('false')
  })

  it('setMode emits the chosen travel mode', async () => {
    const wrapper = mount(RouteFilterBar)
    await buttons(wrapper)[1]!.trigger('click')
    expect(wrapper.emitted('update:mode')?.[0]).toEqual(['bike'])
  })

  it('toggleAda emits the opposite of the current value', async () => {
    const wrapper = mount(RouteFilterBar, { props: { ada: false } })
    await buttons(wrapper)[2]!.trigger('click')
    expect(wrapper.emitted('update:ada')?.[0]).toEqual([true])
  })
})
