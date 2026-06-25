# useTabButton

> 标签按钮组件的 Composable 函数，用于管理标签按钮的状态和事件

**版本**: 1.0.0 | **首次引入**: 1.0.0

## 函数签名

```typescript
function useTabButton(): {
  provideEvent: (e: Function) => void
  injectEvent: () => Function | undefined
  provideActiveItem: (activeItem: Ref<string>) => void
  injectActiveItem: () => Ref<string> | undefined
}
```

## 参数

无参数

## 返回值

**类型**: `Object`

返回一个包含以下方法的对象：

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| provideEvent | e: Function | void | 提供点击事件处理函数 |
| injectEvent | - | Function \| undefined | 注入点击事件处理函数 |
| provideActiveItem | activeItem: Ref<string> | void | 提供活跃项引用 |
| injectActiveItem | - | Ref<string> \| undefined | 注入活跃项引用 |

## 基本用法

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { useTabButton } from '@magustek/framework-ui'

const { provideEvent, provideActiveItem } = useTabButton()
const activeItem = ref('tab1')

// 提供事件处理函数
const handleTabClick = (tabId: string) => {
  activeItem.value = tabId
  console.log('切换到标签:', tabId)
}

provideEvent(handleTabClick)
provideActiveItem(activeItem)
</script>
```

## 示例

### 父组件提供事件和状态

```vue
<template>
  <div class="tab-container">
    <TabButton
      v-for="tab in tabs"
      :key="tab.id"
      :tab-id="tab.id"
      :label="tab.label"
    />
    <div class="tab-content">
      <component :is="activeComponent" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useTabButton } from '@magustek/framework-ui'
import TabButton from './TabButton.vue'
import TabContent1 from './TabContent1.vue'
import TabContent2 from './TabContent2.vue'

const { provideEvent, provideActiveItem } = useTabButton()
const activeItem = ref('tab1')

const tabs = [
  { id: 'tab1', label: '标签 1' },
  { id: 'tab2', label: '标签 2' },
  { id: 'tab3', label: '标签 3' }
]

const activeComponent = computed(() => {
  return activeItem.value === 'tab1' ? TabContent1 : TabContent2
})

const handleTabClick = (tabId: string) => {
  activeItem.value = tabId
}

provideEvent(handleTabClick)
provideActiveItem(activeItem)
</script>

<style scoped>
.tab-container {
  display: flex;
  flex-direction: column;
}

.tab-content {
  flex: 1;
  padding: 16px;
}
</style>
```

### 子组件注入事件和状态

```vue
<template>
  <button
    :class="['tab-button', { active: isActive }]"
    @click="handleClick"
  >
    {{ label }}
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useTabButton } from '@magustek/framework-ui'

defineProps<{
  tabId: string
  label: string
}>()

const { injectEvent, injectActiveItem } = useTabButton()
const clickEvent = injectEvent()
const activeItem = injectActiveItem()

const isActive = computed(() => activeItem?.value === tabId)

const handleClick = () => {
  clickEvent?.(tabId)
}
</script>

<style scoped>
.tab-button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s;
}

.tab-button.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}

.tab-button:hover {
  border-color: #409eff;
}
</style>
```

## 类型定义

```typescript
interface TabButtonContext {
  provideEvent: (e: (tabId: string) => void) => void
  injectEvent: () => ((tabId: string) => void) | undefined
  provideActiveItem: (activeItem: Ref<string>) => void
  injectActiveItem: () => Ref<string> | undefined
}
```

## 依赖

- vue (provide, inject, Ref)

## 注意事项

1. **Provide/Inject 模式** - 该 Composable 使用 Vue 的 Provide/Inject 模式进行跨组件通信
2. **必须在父组件中调用** - `provideEvent` 和 `provideActiveItem` 必须在父组件中调用
3. **子组件中注入** - 子组件通过 `injectEvent` 和 `injectActiveItem` 获取父组件提供的值
4. **响应式引用** - `activeItem` 应该是一个响应式引用，以便实时更新 UI

---

*最后更新: 2026-02-09*
