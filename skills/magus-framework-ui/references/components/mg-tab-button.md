# MgTabButton

标签按钮组件，用于通过数据列表展示多个标签按钮。

用于：标签按钮切换、通过数据驱动按钮组。

---

## Props

| 属性名 | 类型 | 默认值 | 必需 | 说明 |
|--------|------|--------|------|------|
| `span` | `number` | `12` | ❌ | 标题区所占栅格列数（共 24 列），按钮区自动占剩余列 |
| `modelValue` | `string` | `''` | ❌ | 当前激活项，支持 `v-model` 双向绑定 |
| `defaultActive` | `string` | `''` | ❌ | 初始默认激活项，仅在组件挂载时生效 |
| `height` | `string` | `'60px'` | ❌ | 容器高度 |
| `justify` | `'start' \| 'end' \| 'center' \| 'between' \| 'around' \| 'evenly' \| 'stretch'` | `'end'` | ❌ | 按钮区 flex 对齐方式 |


## Slots

| 插槽名 | 说明 |
|--------|------|
| `title` | 标题区内容，位于左侧 |
| `buttons` | 按钮区附加内容，位于 `MgTabButtonItem` 之前 |
| `default` | 默认插槽，通常放入 `MgTabButtonItem` 子组件，位于按钮区 |

## Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| `tabClick` | `(name: string)` | 任一子按钮被点击时触发 |
| `update:modelValue` | `(name: string)` | `v-model` 更新事件 |

## 代码示例

```vue
<template>
  <mg-tab-button v-model="activeTab" :span="8" justify="between" @tab-click="handleTabClick">
    <template #title>
      <span class="text-lg font-bold">数据管理</span>
    </template>
    <template #buttons>
      <el-button type="primary" size="small">新建</el-button>
    </template>
    <mg-tab-button-item name="list" title="列表" />
    <mg-tab-button-item name="detail" title="详情" />
  </mg-tab-button>
</template>

<script setup lang="ts">
const activeTab = ref('list')
const handleTabClick = (name: string) => {
  console.log('点击了:', name)
}
</script>

