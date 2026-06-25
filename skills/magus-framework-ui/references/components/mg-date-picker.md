# MgDatePicker

日期选择器组件，基于 Element Plus `ElDatePicker` 封装。

用于：日期选择、日期范围选择、日期时间选择。

---

## Usage

```vue
<MgDatePicker v-model="date" type="date" placeholder="选择日期" />
```

```ts
import { ref } from 'vue'

const date = ref('')
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| modelValue | `string \| Date` | 否 | `-` | 选中的日期 |
| type | `string` | 否 | `'date'` | 选择器类型：`date` / `daterange` / `datetime` / `datetimerange` |
| placeholder | `string` | 否 | `'选择日期'` | 占位符 |
| disabled | `boolean` | 否 | `false` | 是否禁用 |
| clearable | `boolean` | 否 | `true` | 是否显示清空按钮 |
| format | `string` | 否 | `'YYYY-MM-DD'` | 日期格式 |
| disabledDate | `(date: Date) => boolean` | 否 | `-` | 禁用日期函数 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:modelValue | `string \| Date` | 日期改变时触发 |
| change | `string \| Date` | 日期改变时触发 |
| blur | `void` | 失焦时触发 |
| focus | `void` | 获焦时触发 |

---

## AI Usage Rules

1. `type` 为 `daterange` 或 `datetimerange` 时，`modelValue` 为数组类型。
2. `disabledDate` 函数接收 `Date` 对象，返回 `boolean` 决定该日期是否可选。
3. `format` 使用 dayjs 日期格式字符串。
