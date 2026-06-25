# MgToolbar

工具栏组件，列表页常用的操作栏，默认提供"新增"和"批量删除"按钮，在有选中项时展示已选数量提示。也可以通过默认插槽完全自定义操作区内容。

用于：列表页操作按钮、批量操作、选中数量提示。

---

## Usage

```vue
<MgToolbar :select-length="selected.length" @event-handle="handleToolbarAction" />
```

```ts
const selected = ref<any[]>([])

const handleToolbarAction = (code: string) => {
  if (code === 'add') {
    // 新增
  } else if (code === 'batchDelete') {
    // 批量删除
  }
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| selectLength | `number` | 否 | `0` | 当前选中数量 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| event-handle | `(code: string)` | 默认按钮点击后触发，`code` 为 `add` 或 `batchDelete` |

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| default | `void` | 自定义操作区内容；提供后会覆盖默认按钮，但仍可保留数量提示 |

---

## AI Usage Rules

1. 未提供默认插槽时，会渲染"新增"和"批量删除"两个按钮。
2. `selectLength > 0` 时，才会显示已选数量提示。
3. 默认按钮的国际化文案依赖全局 `$t`。
4. 如需完全自定义按钮顺序或样式，直接使用默认插槽。
