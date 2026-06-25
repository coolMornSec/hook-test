# MgIconPicker

图标选择器组件，用于从图标列表中选取图标。

用于：菜单图标配置、按钮图标选择、图标字段编辑。

---

## Usage

```vue
<MgIconPicker v-model="selectedIcon" @change="handleIconChange" />
```

```ts
import { ref } from 'vue'
import { MgIconPicker } from '@magustek/framework-ui'

const selectedIcon = ref('')

const handleIconChange = (icon: string) => {
  console.log('选择的图标:', icon)
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| modelValue | `string` | 否 | `''` | 选中的图标 |
| icons | `string[]` | 否 | `[]` | 图标列表，数组中的字符串由内部 `mgIcon` 组件渲染 |
| placeholder | `string` | 否 | `'选择图标'` | 占位符 |
| disabled | `boolean` | 否 | `false` | 是否禁用 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:modelValue | `string` | 图标改变时触发 |
| change | `string` | 图标改变时触发 |
