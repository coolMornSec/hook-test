# MgTable

数据表格展示组件，基于 Element Plus `ElTable` 增强，集成分页功能。

用于：表格数据展示、分页、行选择、行展开、排序、过滤。

---

## Usage

```vue
<MgTable
  :data="tableData"
  :total="total"
  v-model:current-page="currentPage"
  v-model:page-size="pageSize"
  @paging-change="handlePagingChange"
>
  <el-table-column prop="id" label="ID" width="80" />
  <el-table-column prop="name" label="名称" />
  <el-table-column prop="status" label="状态" />
</MgTable>
```

```ts
import { ref } from 'vue'

const tableData = ref([
  { id: 1, name: '张三', status: '正常' },
  { id: 2, name: '李四', status: '正常' }
])
const total = ref(100)
const currentPage = ref(1)
const pageSize = ref(20)

const handlePagingChange = (page: number, size: number) => {
  console.log(`切换到第 ${page} 页，每页 ${size} 条`)
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| data | `TableData[]` | 是 | `[]` | 表格数据源 |
| total | `number` | 否 | `0` | 数据总数（用于分页） |
| currentPage | `number` | 否 | `1` | 当前页码 |
| pageSize | `number` | 否 | `20` | 每页显示条数 |
| height | `number \| string` | 否 | `-` | 表格高度，自适应下无须设置，固定高度设置 |
| hidePage | `boolean` | 否 | `false` | 是否隐藏分页器 |
| layout | `string` | 否 | `'sizes, prev, pager, next, jumper'` | 分页器布局 |
| showTip | `boolean` | 否 | `true` | 是否显示分页提示信息 |
| pageSizes | `number[]` | 否 | `[20, 50, 100, 200, 500]` | 每页显示条数选项 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| paging-change | `(currentPage: number, pageSize: number)` | 分页改变时触发 |
| update:currentPage | `number` | 当前页码改变时触发 |
| update:pageSize | `number` | 每页条数改变时触发 |

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| default | `void` | 表格列定义插槽，放置 `el-table-column` |

---

## Methods

通过组件 `ref` 调用。

| 方法名 | 参数 | 返回值 | 说明 |
|---|---|---|---|
| clearSelection | `void` | `void` | 清空表格选择 |
| getSelectionRows | `void` | `TableData[]` | 获取选中的行 |
| toggleRowSelection | `row: TableData, selected: boolean` | `void` | 切换行选择状态 |
| toggleAllSelection | `void` | `void` | 切换全选状态 |
| toggleRowExpansion | `row: TableData, expanded?: boolean` | `void` | 切换行展开状态 |
| setCurrentRow | `row: TableData` | `void` | 设置当前行 |
| clearSort | `void` | `void` | 清空排序 |
| clearFilter | `columnKeys?: string[]` | `void` | 清空过滤 |
| sort | `prop: string, order: string` | `void` | 排序表格 |
| scrollTo | `options: number \| ScrollToOptions, yCoord?: number` | `void` | 滚动到指定位置 |
| setScrollTop | `top?: number` | `void` | 设置垂直滚动位置 |
| setScrollLeft | `left?: number` | `void` | 设置水平滚动位置 |

```vue
<script setup lang="ts">
import { ref } from 'vue'
import type { MgTableInstance } from '@magustek/framework-ui'

const tableRef = ref<MgTableInstance>()

function clearSelection() {
  tableRef.value?.clearSelection()
}

function getSelectedRows() {
  const rows = tableRef.value?.getSelectionRows()
  console.log('选中的行:', rows)
}
</script>
```

---

## Types

```ts
export interface TableData {
  [key: string]: unknown
}

export interface PagingChangePayload {
  currentPage: number
  pageSize: number
}

export interface MgTableInstance {
  clearSelection: () => void
  getSelectionRows: () => TableData[]
  toggleRowSelection: (row: TableData, selected: boolean) => void
  toggleAllSelection: () => void
  toggleRowExpansion: (row: TableData, expanded?: boolean) => void
  setCurrentRow: (row: TableData) => void
  clearSort: () => void
  clearFilter: (columnKeys?: string[]) => void
  sort: (prop: string, order: string) => void
  scrollTo: (options: number | ScrollToOptions, yCoord?: number) => void
  setScrollTop: (top?: number) => void
  setScrollLeft: (left?: number) => void
}
```

---

## AI Usage Rules

1. `data` 为必填项，`total` 仅用于分页计算。
2. `height`在父元素为固定高度可以设置`100%`，父元素为flex表格自适应无须设置`height`。
3. 分页改变时同时监听 `paging-change` 事件和 `update:currentPage` / `update:pageSize`。
4. 表格列通过 `el-table-column` 子组件定义，写在默认插槽中。
5. 调用方法必须通过组件 `ref`。
6. `height` 不设置时表格高度自适应容器，固定高度用数字或字符串（如 `'400px'` 或 `400`）。
