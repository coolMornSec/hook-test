# MgResourceSelect

资源选择器组件，用于从资源库中选择资源。

用于：资源弹窗选择、附件选择、文档关联。

---

## Usage

```vue
<MgResourceSelect
  :resource-code="resourceCode"
  :multiple="true"
  :default-selected="selectedData"
  @confirm="handleConfirm"
/>
```

```ts
import { ref } from 'vue'

const resourceCode = ref('RESOURCE_CODE')
const selectedData = ref<any[]>([])

const handleConfirm = (data: any[]) => {
  console.log('确认选择:', data)
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| title | `string` | 否 | `-` | 标题 |
| placeholder | `string` | 否 | `-` | 占位符 |
| teleported | `boolean` | 否 | `false` | 弹出窗是否插入到 body |
| dialogWidth | `string` | 否 | `'75%'` | 弹窗宽度 |
| dialogVisible | `boolean` | 否 | `false` | 是否显示弹窗 |
| defaultSelected | `any[]` | 否 | `-` | 默认选中的数据 |
| resourceCode | `string` | 否 | `-` | 资源编码 |
| multiple | `boolean` | 否 | `-` | 是否多选 |
| disabled | `boolean` | 否 | `-` | 是否禁用 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:defaultSelected | `any[]` | 默认选中的数据发生变化 |
| update:dialogVisible | `boolean` | 弹窗显示状态变化 |
| confirm | `any[]` | 确认选择时触发 |

---

## Types

```ts
export interface MgResourceSelectProps {
  title?: string
  placeholder?: string
  teleported?: boolean
  dialogWidth?: string
  dialogVisible?: boolean
  defaultSelected?: any[]
  resourceCode?: string
  multiple?: boolean
  disabled?: boolean
}
```

---

## AI Usage Rules

1. `resourceCode` 为后端定义的资源编码，用于筛选可选资源范围。
2. `defaultSelected` 用于回显已选数据。
3. `confirm` 事件在用户点击确认按钮后触发，传递选中的资源数据。
4. `dialogVisible` 支持 `.sync` 修饰符或 `v-model` 控制弹窗显示。

---
