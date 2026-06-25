# MgCascader

级联选择器组件，基于 Element Plus `ElCascader` 封装。

用于：省市区选择、组织架构选择、多级分类选择。

---

## Usage

```vue
<MgCascader v-model="selectedValue" :options="options" @change="handleChange" />
```

```ts
import { ref } from 'vue'

const selectedValue = ref<string[]>([])

const options = [
  {
    value: 'zhejiang',
    label: '浙江',
    children: [
      {
        value: 'hangzhou',
        label: '杭州',
        children: [
          { value: 'xihu', label: '西湖' }
        ]
      }
    ]
  }
]

const handleChange = (value: string[]) => {
  console.log('选择值:', value)
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| options | `CascaderOption[]` | 是 | `[]` | 级联数据源 |
| modelValue | `Array` | 否 | `[]` | 选中的值 |
| props | `object` | 否 | `-` | 数据字段映射配置 |
| placeholder | `string` | 否 | `'请选择'` | 占位符 |
| disabled | `boolean` | 否 | `false` | 是否禁用 |
| clearable | `boolean` | 否 | `true` | 是否显示清空按钮 |
| filterable | `boolean` | 否 | `false` | 是否可搜索 |
| multiple | `boolean` | 否 | `false` | 是否多选 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:modelValue | `Array` | 选中值改变时触发 |
| change | `Array` | 选中值改变时触发 |
| blur | `void` | 失焦时触发 |
| focus | `void` | 获焦时触发 |

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| default | `void` | 自定义内容 |

---

## AI Usage Rules

1. `options` 为必填项，数据结构默认使用 `value`、`label`、`children` 字段。
2. `props` 用于自定义 `options` 中的数据字段映射，如 `{ value: 'id', label: 'name', children: 'childList' }`。
3. `multiple` 为 `true` 时，`modelValue` 为二维数组。
4. `filterable` 为 `true` 时支持在选项中搜索过滤。
