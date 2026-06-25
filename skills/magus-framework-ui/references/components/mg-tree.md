# MgTree

树形结构展示与操作组件，基于 Element Plus `ElTree` 增强。

用于：树数据展示、节点搜索、刷新、展开收缩、添加、编辑、删除、自定义节点内容。

---

## Usage

```vue
<MgTree
  :data="treeData"
  node-key="nodeId"
  :props="treeProps"
  :is-edit="true"
  :is-need-search="true"
  :is-need-reload="true"
  :icon-list="iconList"
  @node-click="handleNodeClick"
  @reload-tree="handleReloadTree"
  @add-node="handleAddNode"
  @edit-node="handleEditNode"
  @delete-node="handleDeleteNode"
/>
```

```ts
const treeProps = {
  children: 'children',
  label: 'text',
  disabled: 'disabled'
}
const iconList = ['wenjianjia1', 'bumenyongneng']
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| data | `TreeNodeData[]` | 是 | `[]` | 树形数据源 |
| isEdit | `boolean` | 否 | `true` | 是否启用编辑模式，控制添加、编辑、删除按钮 |
| isNeedReload | `boolean` | 否 | `true` | 是否显示刷新按钮 |
| isNeedSearch | `boolean` | 否 | `true` | 是否显示搜索框 |
| isNeedExpand | `boolean` | 否 | `true` | 是否显示展开 / 收缩按钮 |
| highlight | `boolean` | 否 | `true` | 是否高亮选中节点 |
| nodeKey | `string` | 否 | `'nodeId'` | 节点唯一标识字段 |
| defaultExpandAll | `boolean` | 否 | `false` | 是否默认展开全部节点 |
| defaultExpandedKeys | `(string \| number)[]` | 否 | `[]` | 默认展开的节点 key 列表 |
| showLine | `boolean` | 否 | `true` | 是否显示树形连接线 |
| showLabelLine | `boolean` | 否 | `false` | 节点 label 是否显示连接线 |
| props | `TreeFieldProps` | 否 | `{ children: 'children', label: 'text', disabled: 'disabled' }` | 节点字段映射 |
| matchCase | `boolean` | 否 | `true` | 搜索时是否区分大小写 |
| filterPlaceeHolder | `string` | 否 | `'请输入节点名称'` | 搜索框占位符 |
| icon | `string` | 否 | `''` | 统一节点图标 |
| iconSpin | `boolean` | 否 | `true` | 节点展开收缩时图标是否旋转 |
| iconList | `string[]` | 否 | `[]` | 自定义节点图标列表，数组中的字符串由 tree 内部的 `mgIcon` 组件进行渲染 |
| magusIconClass | `TreeNodeIconClassGetter` | 否 | `-` | 自定义图标类名函数 |
| magusIconStyle | `TreeNodeIconStyle \| TreeNodeIconStyleGetter` | 否 | `-` | 自定义图标样式 |
| nodeIsNeedAdd | `boolean \| TreeNodeVisibleGetter` | 否 | `true` | 节点是否显示添加按钮 |
| nodeIsNeedEdit | `boolean \| TreeNodeVisibleGetter` | 否 | `true` | 节点是否显示编辑按钮 |
| nodeIsNeedDelete | `boolean \| TreeNodeVisibleGetter` | 否 | `true` | 节点是否显示删除按钮 |


---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| node-click | `TreeNodeActionPayload` | 节点被点击时触发 |
| reload-tree | `void` | 点击刷新按钮时触发 |
| add-node | `TreeNodeActionPayload` | 点击添加按钮时触发 |
| edit-node | `TreeNodeActionPayload` | 点击编辑按钮时触发 |
| delete-node | `TreeNodeActionPayload` | 点击删除按钮时触发 |
| node-dbl-click | `TreeNodeInstance` | 节点被双击时触发 |

### Event Rules

当前节点操作事件参数是扁平结构：

```ts
type TreeNodeActionPayload = TreeNodeData & {
  node: TreeNodeInstance
}
```

也就是：

```ts
{ ...data,node }
```

不要写成：

```ts
{ data, node }
```

`reload-tree` 无参数。

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| default | `{ node, data }` | 自定义节点内容 |
| treeButton | `void` | 顶部工具栏右侧自定义按钮 |
| customButton | `{ data, node }` | 节点右侧自定义按钮 |
| empty | `void` | 空状态内容 |
| treeFooter | `void` | 树底部内容 |

### Slot Example

```vue
<MgTree :data="treeData">
  <template #default="{ node, data }">
    <span>{{ data.text }}</span>
  </template>

  <template #customButton="{ data, node }">
    <el-button link type="primary" @click.stop="handleDetail(data, node)">
      详情
    </el-button>
  </template>
</MgTree>
```

节点按钮建议使用 `@click.stop`，避免触发节点点击事件。

---

## Methods

通过组件 `ref` 调用。

| 方法名 | 参数 | 返回值 | 说明 |
|---|---|---|---|
| goFilterText | `val: string` | `void` | 主动过滤树节点 |
| setCurrentKey | `key: string \| number` | `void` | 选中指定节点 |
| setCheckedKeys | `keys: (string \| number)[]` | `void` | 设置 checkbox 选中节点 |
| getCheckedNodes | `leafOnly?: boolean, includeHalfChecked?: boolean` | `TreeNodeData[]` | 获取选中节点 |

```vue
<script setup lang="ts">
import { ref } from 'vue'

const treeRef = ref<MgTreeInstance>()

function selectNode(id: string) {
  treeRef.value?.setCurrentKey(id)
}

function filterTree(keyword: string) {
  treeRef.value?.goFilterText(keyword)
}
</script>
```

---

## Types

```ts
export type TreeNodeKey = string | number

export interface TreeNodeData {
  nodeId?: TreeNodeKey
  text?: string
  children?: TreeNodeData[]
  disabled?: boolean
  icon?: string
  [key: string]: unknown
}

export interface TreeFieldProps {
  children: string
  label: string
  disabled: string
}

export interface TreeNodeInstance {
  id?: TreeNodeKey
  key?: TreeNodeKey
  level?: number
  expanded?: boolean
  checked?: boolean
  disabled?: boolean
  data?: TreeNodeData
  [key: string]: unknown
}

export type TreeNodeActionPayload = TreeNodeData & {
  node: TreeNodeInstance
}

export type TreeNodeVisibleGetter = (
  data: TreeNodeData,
  node: TreeNodeInstance
) => boolean

export type TreeNodeIconStyle = Record<string, string | number>

export type TreeNodeIconClassGetter = (
  data: TreeNodeData,
  node: TreeNodeInstance
) => string

export type TreeNodeIconStyleGetter = (
  data: TreeNodeData,
  node: TreeNodeInstance
) => TreeNodeIconStyle

export interface MgTreeInstance {
  goFilterText: (val: string) => void
  setCurrentKey: (key: TreeNodeKey) => void
  setCheckedKeys: (keys: TreeNodeKey[]) => void
  getCheckedNodes: (
    leafOnly?: boolean,
    includeHalfChecked?: boolean
  ) => TreeNodeData[]
}
```

---

## AI Usage Rules

1. 如果后端字段不同，必须配置 `nodeKey` 和 `props`。
2. `node-click`、`add-node`、`edit-node`、`delete-node` 的参数是 `{ ...data, node }`。
3. `node-dbl-click` 参数是 `node`。
4. 调用方法必须使用组件 `ref`。
5. 自定义节点右侧按钮应使用 `@click.stop`。
6. 添加、编辑、删除按钮显示时必须同时考虑 `isEdit` 和对应的 `nodeIsNeedXxx`。