# TreePropType 类型

> 树形组件属性映射类型定义

**版本**: 1.0.0 | **首次引入**: 1.0.0

## 类型定义

```typescript
export interface TreePropType {
  data: AnyObject[]
  nodeKey?: string
  children?: string
  label?: string
  disabled?: string
  isLeaf?: string
}
```

## 属性说明

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| data | AnyObject[] | - | 树形数据源 |
| nodeKey | string | 'id' | 树节点的唯一标识属性名 |
| children | string | 'children' | 树节点的子节点属性名 |
| label | string | 'label' | 树节点的标签属性名 |
| disabled | string | 'disabled' | 树节点的禁用属性名 |
| isLeaf | string | 'isLeaf' | 树节点的叶子节点属性名 |

## 使用示例

### 基础用法

```typescript
import type { TreePropType } from '@magustek/framework-ui'

const treeProps: TreePropType = {
  data: [],
  nodeKey: 'id',
  children: 'children',
  label: 'name',
  disabled: 'disabled',
  isLeaf: 'isLeaf'
}
```

### 在组件中使用

```vue
<template>
  <MgTree
    :data="treeData"
    :props="treeProps"
    @node-click="handleNodeClick"
  />
</template>

<script setup lang="ts">
import type { TreePropType } from '@magustek/framework-ui'
import { MgTree } from '@magustek/framework-ui'

const treeProps: TreePropType = {
  data: [],
  nodeKey: 'id',
  children: 'subItems',
  label: 'title',
  disabled: 'isDisabled'
}

const treeData = ref([
  {
    id: 1,
    title: '一级菜单',
    subItems: [
      { id: 11, title: '二级菜单 1' },
      { id: 12, title: '二级菜单 2', isDisabled: true }
    ]
  },
  {
    id: 2,
    title: '一级菜单 2',
    subItems: [
      { id: 21, title: '二级菜单 3' }
    ]
  }
])

const handleNodeClick = (data) => {
  console.log('点击节点:', data)
}
</script>
```

### 自定义属性映射

```typescript
// 当数据结构与默认属性名不同时，可以自定义映射
const customTreeProps: TreePropType = {
  data: myTreeData,
  nodeKey: 'nodeId',        // 使用 nodeId 作为唯一标识
  children: 'childNodes',   // 使用 childNodes 作为子节点属性
  label: 'nodeName',        // 使用 nodeName 作为显示标签
  disabled: 'isDisabled',   // 使用 isDisabled 作为禁用标志
  isLeaf: 'leaf'            // 使用 leaf 作为叶子节点标志
}
```

### 处理异步加载

```vue
<template>
  <MgTree
    :data="treeData"
    :props="treeProps"
    :load="loadNode"
    lazy
  />
</template>

<script setup lang="ts">
import type { TreePropType } from '@magustek/framework-ui'

const treeProps: TreePropType = {
  data: [],
  nodeKey: 'id',
  children: 'children',
  label: 'name',
  isLeaf: 'leaf'
}

const loadNode = (node, callback) => {
  // 异步加载子节点
  setTimeout(() => {
    callback([
      { id: Math.random(), name: '动态节点 1', leaf: true },
      { id: Math.random(), name: '动态节点 2', leaf: false }
    ])
  }, 1000)
}
</script>
```

## 相关类型

- [CropperConfig](./cropper-config.md) - 裁剪器配置类型
- [CropperRealTimeData](./cropper-real-time-data.md) - 裁剪实时数据类型

## 相关组件

- [MgTree](../components/mg-tree.md) - 树形组件

---

*此文档由 Framework-UI API 文档生成器自动生成*
*最后更新: 2026-02-09*
