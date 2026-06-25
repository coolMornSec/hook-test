# MgTabs

标签页组件，基于 Element Plus `ElTabs` 封装。与 `MgTabPane` 配合使用。

用于：多标签页切换、可关闭标签、可添加标签。

---

## Usage

```vue
<MgTabs v-model="activeTab">
  <MgTabPane label="标签 1" name="tab1">
    <div>标签 1 的内容</div>
  </MgTabPane>
  <MgTabPane label="标签 2" name="tab2">
    <div>标签 2 的内容</div>
  </MgTabPane>
</MgTabs>
```

```ts
import { ref } from 'vue'
const activeTab = ref('tab1')
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| modelValue | `string` | 否 | `''` | 活跃标签名 |
| type | `string` | 否 | `'card'` | 标签页类型 |
| closable | `boolean` | 否 | `false` | 标签页是否可关闭 |
| addable | `boolean` | 否 | `false` | 是否可添加标签页 |
| editable | `boolean` | 否 | `false` | 标签页是否可编辑 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:modelValue | `string` | 活跃标签改变时触发 |
| tab-change | `string` | 标签改变时触发 |
| tab-add | `void` | 添加标签页时触发 |
| tab-remove | `string` | 移除标签页时触发 |
