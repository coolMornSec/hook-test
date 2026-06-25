# MgTabPane

标签页项组件，与 `MgTabs` 组件配合使用。

用于：定义单个标签页的内容和标题。

---

## Usage

```vue
<MgTabs>
  <MgTabPane label="标签 1" name="tab1">
    <div>标签 1 的内容</div>
  </MgTabPane>
  <MgTabPane label="标签 2" name="tab2">
    <div>标签 2 的内容</div>
  </MgTabPane>
</MgTabs>
```

```ts
import { MgTabs, MgTabPane } from '@magustek/framework-ui'
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| label | `string` | 是 | `''` | 标签页标题 |
| name | `string` | 是 | `''` | 标签页名称 |
| disabled | `boolean` | 否 | `false` | 是否禁用 |
| closable | `boolean` | 否 | `false` | 是否可关闭 |
| lazy | `boolean` | 否 | `false` | 是否延迟加载 |

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| default | `void` | 标签页内容 |
| label | `void` | 标签页标题 |
