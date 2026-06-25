# MgComplexSelect

用户部门选择器组件，支持跨类型（用户、组织、工作组、职务、关系）选择人员或组织。

用于：人员选择、部门选择、审批人选择、跨类型多来源选择。

---

## Usage

```vue
<MgComplexSelect
  :select-types="selectTypes"
  :default-selected="selectedData"
  @confirm="onConfirmSelect"
/>
```

```ts
const selectTypes = ref<SelectTypes>([
  { type: '$USER', multiple: true },
  { type: '$ORG', multiple: false, withDuty: true },
  { type: '$WORKGROUP', multiple: false },
  { type: '$DUTY', multiple: true },
  { type: '$RELATION', multiple: false, withDuty: true },
])

const selectedData = ref<DefaultSelected>({})

const onConfirmSelect = (data: DefaultSelected) => {
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
| crossSelect | `boolean` | 否 | `false` | 是否允许跨类型选择 |
| selectTypes | `SelectTypes` | 是 | `[{ type: '$USER', multiple: true }]` | 选择类型配置列表 |
| defaultSelected | `DefaultSelected` | 否 | `{}` | 默认选中的数据 |
| defaultTab | `SelectTypeName` | 否 | `-` | 默认选中的 Tab |
| multiple | `boolean` | 否 | `false` | 是否多选 |
| compCode | `string` | 否 | `-` | 公司编码 |
| compId | `string` | 否 | `-` | 公司 ID |
| disabled | `boolean` | 否 | `false` | 是否禁用 |
| dataType | `SelectTypeName` | 否 | `-` | 数据类型 |
| defaultValue | `string` | 否 | `-` | 默认值 |
| defaultLabel | `string` | 否 | `-` | 默认标签值 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:defaultSelected | `DefaultSelected` | 默认选中的数据发生变化 |
| update:dialogVisible | `boolean` | 弹窗显示状态变化 |
| update:defaultValue | `string` | 默认值发生变化 |
| update:defaultLabel | `string` | 默认标签值发生变化 |
| confirm | `DefaultSelected` | 确认选择时触发 |

---

## Types

```ts
type SelectTypeName = '$USER' | '$ORG' | '$WORKGROUP' | '$DUTY' | '$RELATION'

type SelectTypes = Array<{
  type: SelectTypeName
  label?: string
  multiple?: boolean
  limit?: number
  withDuty?: boolean
  requireDuty?: boolean
  limitDuty?: number
  showCheckbox?: boolean
  checkStrictly?: boolean
}>

type DefaultSelected = {
  [key in SelectTypeName]?: Array<{
    id: string
    name: string
    duty?: Array<{
      id: string
      name: string
    }>
  }>
}
```

---

## AI Usage Rules

1. `selectTypes` 为必填项，定义选择器 Tab 和每个 Tab 的配置。
2. `SelectTypeName` 有五种类型：`$USER`（用户）、`$ORG`（组织）、`$WORKGROUP`（工作组）、`$DUTY`（职务）、`$RELATION`（关系）。
3. `withDuty` 为 `true` 时，选择组织后需要额外选择职务。
4. `crossSelect` 为 `true` 时允许跨类型混合选择。
5. `confirm` 事件在用户点击确认后触发，传递的数据结构为 `DefaultSelected`。
6. `defaultSelected` 用于回显已选数据，数据结构需与 `DefaultSelected` 一致。
