# MgDict

字典组件，根据字典编码 `dictCode` 自动请求并渲染对应字典项的下拉选择或级联选择。

用于：业务字典下拉选择、字典级联选择。

---

## Usage

```vue
<MgDict v-model="modelValue" dict-code="STATUS" />
```

```ts
import { ref } from 'vue'

const modelValue = ref('')
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| dictCode | `string` | 是 | `-` | 字典编码，用于请求后端字典数据 |
| dictType | `'select' \| 'cascader'` | 否 | `'select'` | 字典类型：`select` 为下拉选择，`cascader` 为级联选择 |

此外，组件透传 Element Plus `ElSelect` / `ElCascader` 原生属性（如 `placeholder`、`disabled`、`clearable`、`multiple` 等）。

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:modelValue | `string \| string[]` | 选中值改变时触发 |

---

## AI Usage Rules

1. `dictCode` 为必填项，传入后端定义的字典编码。
2. `dictType` 为 `'select'` 时渲染为 `el-select`，为 `'cascader'` 时渲染为 `el-cascader`。
3. 组件自动根据 `dictCode` 请求后端字典接口获取选项数据。
4. 可透传 Element Plus 原生属性（`placeholder`、`disabled`、`clearable`、`multiple` 等）。
