# MgTimePicker

时间选择器组件，基于 Element Plus `ElTimePicker` 封装。

用于：时间选择、时间范围选择。

---

## Usage

```vue
<MgTimePicker v-model="time" placeholder="选择时间" />
```

```ts
import { ref } from 'vue'
const time = ref('')
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| modelValue | `string` | 否 | `-` | 选中的时间 |
| placeholder | `string` | 否 | `'选择时间'` | 占位符 |
| disabled | `boolean` | 否 | `false` | 是否禁用 |
| clearable | `boolean` | 否 | `true` | 是否显示清空按钮 |
| format | `string` | 否 | `'HH:mm:ss'` | 时间格式 |
| isRange | `boolean` | 否 | `false` | 是否为时间范围选择 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:modelValue | `string` | 时间改变时触发 |
| change | `string` | 时间改变时触发 |
