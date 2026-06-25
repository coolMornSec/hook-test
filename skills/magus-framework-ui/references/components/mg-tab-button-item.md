# MgTabButtonItem

标签按钮项组件，与 `MgTabButton` 组件配合使用，或可独立通过 `v-for` 渲染。

用于：单个标签按钮项。

---

## Props

| 属性名 | 类型 | 默认值 | 必需 | 说明 |
|--------|------|--------|------|------|
| `title` | `string` | `''` | ❌ | 按钮标题，也可通过默认插槽自定义内容 |
| `name` | `string` | `''` | ✅ | 按钮唯一标识，用于匹配激活状态 |

## 插槽

| 插槽名 | 说明 |
|--------|------|
| `default` | 自定义按钮内容，优先级高于 `title` 属性 |

## 代码示例

```vue
<template>
  <mg-tab-button v-model="activeTab">
    <mg-tab-button-item name="tab1" title="标签1" />
    <mg-tab-button-item name="tab2" title="标签2" />
    <mg-tab-button-item name="tab3" title="标签3" />
  </mg-tab-button>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MgTabButton, MgTabButtonItem } from '@magustek/framework-ui'

const activeTab = ref('tab1')
</script>
```

---
