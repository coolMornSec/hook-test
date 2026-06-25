# useMgIcon 组合式函数

> 用于管理和使用框架内置图标的组合式函数

## 基本用法

```typescript
import { useMgIcon } from '@magustek/framework-ui'

const { getIcon, hasIcon, getAllIcons } = useMgIcon()
```

## 返回值

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| getIcon | name: string | string \| undefined | 获取指定名称的图标 |
| hasIcon | name: string | boolean | 检查图标是否存在 |
| getAllIcons | - | string[] | 获取所有可用的图标列表 |

## 示例

### 基础用法

```vue
<template>
  <div>
    <!-- 使用图标 -->
    <i :class="getIcon('add')" />
    <i :class="getIcon('delete')" />
    <i :class="getIcon('edit')" />
  </div>
</template>

<script setup lang="ts">
import { useMgIcon } from '@magustek/framework-ui'

const { getIcon } = useMgIcon()
</script>
```

### 检查图标是否存在

```vue
<template>
  <div>
    <button v-if="hasIcon('save')">
      <i :class="getIcon('save')" /> 保存
    </button>
    <button v-else>
      保存
    </button>
  </div>
</template>

<script setup lang="ts">
import { useMgIcon } from '@magustek/framework-ui'

const { getIcon, hasIcon } = useMgIcon()
</script>
```

### 获取所有可用图标

```vue
<template>
  <div>
    <h3>可用图标列表</h3>
    <div class="icon-grid">
      <div v-for="iconName in allIcons" :key="iconName" class="icon-item">
        <i :class="getIcon(iconName)" />
        <span>{{ iconName }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMgIcon } from '@magustek/framework-ui'

const { getIcon, getAllIcons } = useMgIcon()
const allIcons = getAllIcons()
</script>

<style scoped>
.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
}

.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
```

### 在组件中使用

```vue
<template>
  <div class="toolbar">
    <button @click="handleAdd">
      <i :class="getIcon('add')" /> 添加
    </button>
    <button @click="handleEdit">
      <i :class="getIcon('edit')" /> 编辑
    </button>
    <button @click="handleDelete">
      <i :class="getIcon('delete')" /> 删除
    </button>
    <button @click="handleSave">
      <i :class="getIcon('save')" /> 保存
    </button>
  </div>
</template>

<script setup lang="ts">
import { useMgIcon } from '@magustek/framework-ui'

const { getIcon } = useMgIcon()

const handleAdd = () => {
  console.log('添加')
}

const handleEdit = () => {
  console.log('编辑')
}

const handleDelete = () => {
  console.log('删除')
}

const handleSave = () => {
  console.log('保存')
}
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 10px;
}

button {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

button:hover {
  background: #f5f5f5;
}
</style>
```

## 相关函数

- [useSvg](./use-svg.md) - SVG 资源管理函数
- [useMgUiMsg](./use-mg-ui-msg.md) - 国际化消息管理函数

---

_最后更新: 2026-05-18_
