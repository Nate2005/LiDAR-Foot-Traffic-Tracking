import { describe, it, expect, beforeEach } from 'vitest'
import { nextTick } from 'vue'
import { mount } from '@vue/test-utils'
import SearchPanel from '../components/SearchPanel.vue'

describe('SearchPanel', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('prefills From with the current location and leaves To blank', async () => {
    const wrapper = mount(SearchPanel)
    await nextTick()
    expect((wrapper.find('input[aria-label="From"]').element as HTMLInputElement).value).toBe(
      'Current location',
    )
    expect((wrapper.find('input[aria-label="To"]').element as HTMLInputElement).value).toBe('')
  })

  it('filters buildings as the user types', async () => {
    const wrapper = mount(SearchPanel)
    const input = wrapper.find('input[aria-label="To"]')
    await input.setValue('pennington')
    const items = wrapper.findAll('.item')
    expect(items).toHaveLength(1)
    expect(items[0]!.text()).toContain('Pennington')
  })

  it('selecting a building emits a route request', async () => {
    const wrapper = mount(SearchPanel)
    await wrapper.find('input[aria-label="To"]').setValue('crowley')
    await wrapper.find('.item').trigger('mousedown')

    const emitted = wrapper.emitted('route')
    expect(emitted).toBeTruthy()
    expect(emitted![emitted!.length - 1]).toEqual([{ fromId: null, toId: 'joe-crowley-union' }])
  })

  it('shows recent searches (most recent first, max 5) when the field is empty', async () => {
    const wrapper = mount(SearchPanel)
    const names = ['pennington', 'crowley', 'knowledge', 'davidson', 'ansari', 'lawlor']
    for (const n of names) {
      await wrapper.find('input[aria-label="To"]').setValue(n)
      await wrapper.find('.item').trigger('mousedown')
    }
    await wrapper.find('input[aria-label="To"]').setValue('')
    const items = wrapper.findAll('.item')
    expect(items).toHaveLength(5)
    expect(items[0]!.text()).toContain('Lawlor')
  })
})
