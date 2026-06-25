# MgAddTemplate

添加模板对话框组件，用于从模板列表中选择模板进行添加。

用于：模板选择、从模板创建新记录。

---

## Usage

```vue
<MgAddTemplate v-model="visible" :templates="templates" @select="handleSelect" />
```

```ts
import { ref } from 'vue'
import { MgAddTemplate } from '@magustek/framework-ui'

const visible = ref(false)

const templates = [
  { id: 1, name: '模板1', description: '描述1' },
  { id: 2, name: '模板2', description: '描述2' }
]

const handleSelect = (template: object) => {
  console.log('选择模板:', template)
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| modelValue | `boolean` | 否 | `false` | 对话框是否显示 |
| templates | `Array` | 是 | `[]` | 模板列表 |
| title | `string` | 否 | `'添加模板'` | 对话框标题 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:modelValue | `boolean` | 对话框显示/隐藏状态改变时触发 |
| select | `object` | 选择模板时触发 |

---

## AI Usage Rules

1. `templates` 为必填项，数组中的每个模板对象需包含 `id` 和 `name` 等字段。
2. 使用 `v-model` 控制对话框的显示和隐藏。
3. `select` 事件在选择模板后触发，传递选中的模板对象。
