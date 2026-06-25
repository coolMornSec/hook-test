# Composable 函数

> Framework-UI 提供的 Vue 3 Composable 函数集合

## 📋 函数列表

### 状态管理

- **[useTabButton](./use-tab-button.md)** - 标签按钮组件的状态管理函数

### 图标管理

- **[useMgIcon](./use-mg-icon.md)** - 框架内置图标管理函数

### 国际化

- **[useMgUiMsg](./use-mg-ui-msg.md)** - 国际化消息管理函数

## 🚀 快速开始

### 导入 Composable

```typescript
import { useTabButton } from '@magustek/framework-ui'
```

### 在组件中使用

```vue
<script setup lang="ts">
import { useTabButton } from '@magustek/framework-ui'

const { provideEvent, injectEvent } = useTabButton()
</script>
```

## 📖 使用示例

### useTabButton 示例

```vue
<template>
  <div class="tabs">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      :class="{ active: activeTab === tab.id }"
      @click="activeTab = tab.id"
    >
      {{ tab.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTabButton } from '@magustek/framework-ui'

const { provideEvent, provideActiveItem } = useTabButton()
const activeTab = ref('tab1')

const tabs = [
  { id: 'tab1', label: '标签 1' },
  { id: 'tab2', label: '标签 2' }
]

provideEvent((tabId) => {
  activeTab.value = tabId
})
provideActiveItem(activeTab)
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 8px;
}

button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: #fff;
  cursor: pointer;
}

button.active {
  background: #409eff;
  color: #fff;
}
</style>
```

## 🎯 最佳实践

1. **在父组件中提供** - 在需要共享状态的父组件中调用 `provide*` 方法
2. **在子组件中注入** - 在子组件中调用 `inject*` 方法获取共享状态
3. **使用响应式引用** - 确保使用 `ref` 创建响应式数据
4. **错误处理** - 检查注入的值是否存在，避免 undefined 错误

## 📚 更多资源

- [Vue 3 Composables 官方文档](https://vuejs.org/guide/reusability/composables.html)
- [Provide/Inject 模式](https://vuejs.org/guide/components/provide-inject.html)

---

*此文档由 Framework-UI API 文档生成器自动生成*
*最后更新: 2026-02-09*
