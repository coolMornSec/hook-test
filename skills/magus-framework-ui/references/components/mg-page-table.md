# MgPageTable

完整的分页表格组件，集成搜索表单、工具栏、表格和分页功能。基于 `MgLayout` 构建。

用于：带搜索的列表页、CRUD 管理页、数据查询分页展示。

---

## Usage

```vue
<MgPageTable
  :data="tableData"
  :total="totalCount"
  :loading="loading"
  v-model:current-page="currentPage"
  v-model:page-size="pageSize"
  :add-method="handleAdd"
  :delete-method="handleDelete"
  @search="handleSearch"
  @paging-change="handlePagingChange"
  @selection-change="handleSelectionChange"
>
  <template #search>
    <el-form-item label="用户名">
      <el-input v-model="searchForm.username" placeholder="请输入用户名" />
    </el-form-item>
    <el-form-item label="状态">
      <el-select v-model="searchForm.status" placeholder="请选择状态">
        <el-option label="激活" value="active" />
        <el-option label="禁用" value="inactive" />
      </el-select>
    </el-form-item>
  </template>
  <template #table>
    <el-table-column type="selection" width="55" />
    <el-table-column prop="id" label="ID" width="80" />
    <el-table-column prop="username" label="用户名" min-width="120" />
    <el-table-column prop="status" label="状态" min-width="100" />
    <el-table-column label="操作" width="200" fixed="right">
      <template #default="{ row }">
        <MgButton type="primary" size="small" @click="handleEdit(row)">编辑</MgButton>
        <MgButton type="danger" size="small" @click="handleDeleteRow(row)">删除</MgButton>
      </template>
    </el-table-column>
  </template>
</MgPageTable>
```

```ts
import { reactive, ref } from 'vue'
import { MgPageTable } from '@magustek/framework-ui'

const currentPage = ref(1)
const pageSize = ref(20)
const totalCount = ref(0)
const loading = ref(false)
const tableData = ref<any[]>([])

const searchForm = reactive({
  username: '',
  status: ''
})

const handleSearch = async () => {
  loading.value = true
  // 调用 API 获取数据
  loading.value = false
}

const handlePagingChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  handleSearch()
}

const handleSelectionChange = (selection: any[]) => {
  console.log('选中行:', selection)
}

const handleAdd = () => {
  // 打开新增对话框
}

const handleDelete = () => {
  // 批量删除选中行
}

const handleEdit = (row: any) => {
  // 打开编辑对话框
}

const handleDeleteRow = (row: any) => {
  // 删除单行
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| data | `any[]` | 是 | `[]` | 表格数据源 |
| deleteMethod | `() => void` | 是 | `-` | 删除按钮点击回调 |
| total | `number` | 否 | `0` | 数据总数 |
| currentPage | `number` | 否 | `1` | 当前页码 |
| pageSize | `number` | 否 | `100` | 每页条数 |
| loading | `boolean` | 否 | `false` | 是否加载中 |
| gap | `string` | 否 | `'16px'` | 区域间距 |
| showMore | `boolean` | 否 | `false` | 是否显示更多搜索选项 |
| showSearchIcon | `boolean` | 否 | `false` | 是否显示搜索图标 |
| labelWidth | `number` | 否 | `100` | 搜索表单标签宽度 |
| showButtons | `boolean` | 否 | `true` | 是否显示搜索按钮 |
| contentGrowth | `boolean` | 否 | `false` | 搜索表单是否自适应增长 |
| isExpand | `boolean` | 否 | `false` | 搜索表单是否默认展开 |
| stripe | `boolean` | 否 | `false` | 是否显示斑马纹 |
| highlightCurrentRow | `boolean` | 否 | `false` | 是否高亮当前行 |
| hideBtn | `boolean` | 否 | `false` | 是否隐藏工具栏 |
| hidePage | `boolean` | 否 | `false` | 是否隐藏分页 |
| hideSearch | `boolean` | 否 | `false` | 是否隐藏搜索表单 |
| rowKey | `string` | 否 | `'id'` | 行唯一标识字段 |
| expandRowKeys | `string[]` | 否 | `[]` | 默认展开的行 |
| showAddBtn | `boolean` | 否 | `true` | 是否显示新增按钮 |
| showDeleteBtn | `boolean` | 否 | `true` | 是否显示删除按钮 |
| addMethod | `() => void` | 否 | `-` | 新增按钮点击回调 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| search | `void` | 搜索时触发 |
| paging-change | `(currentPage: number, pageSize: number)` | 分页变化时触发 |
| selection-change | `selection: any[]` | 表格选择变化时触发 |
| row-click | `row: any` | 行被点击时触发 |
| update:currentPage | `number` | 当前页码变化时触发 |
| update:pageSize | `number` | 每页条数变化时触发 |

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| search | `void` | 搜索表单内容，放置 `el-form-item` |
| more | `void` | 更多搜索选项（需配合 `showMore`） |
| buttons | `void` | 工具栏自定义按钮 |
| table | `void` | 表格列定义，放置 `el-table-column` |

---

## Methods

通过组件 `ref` 调用。

| 方法名 | 参数 | 返回值 | 说明 |
|---|---|---|---|
| tableRef | `void` | `MgTableInstance` | 获取内部 `MgTable` 组件的 ref |

---

## Types

```ts
export interface MgPageTableProps {
  data: any[]
  deleteMethod: () => void
  total?: number
  currentPage?: number
  pageSize?: number
  loading?: boolean
  gap?: string
  showMore?: boolean
  showSearchIcon?: boolean
  labelWidth?: number
  showButtons?: boolean
  contentGrowth?: boolean
  isExpand?: boolean
  stripe?: boolean
  highlightCurrentRow?: boolean
  hideBtn?: boolean
  hidePage?: boolean
  hideSearch?: boolean
  rowKey?: string
  expandRowKeys?: string[]
  showAddBtn?: boolean
  showDeleteBtn?: boolean
  addMethod?: () => void
}

export interface MgPageTableInstance {
  tableRef: () => MgTableInstance | undefined
}
```

---

## AI Usage Rules

1. `data` 和 `deleteMethod` 为必填项。
2. 搜索表单内容通过 `search` 插槽自定义，搜索时会重置当前页为 1。
3. 分页变化时会自动触发搜索，无需手动调用。
4. 表格列定义通过 `table` 插槽提供，使用 Element Plus 的 `el-table-column`。
5. 新增按钮的回调通过 `addMethod` prop 传入，删除按钮的回调通过 `deleteMethod` 传入。
6. 不常用的搜索字段放在 `more` 插槽中，需同时设置 `showMore` 为 `true`。
7. 通过 `tableRef` 方法可获取内部 `MgTable` 实例，调用其方法（如 `clearSelection`、`getSelectionRows`）。
8. `loading` 为 `true` 时会在整个组件上显示加载遮罩。
