# Framework-UI 最佳实践指南

## 阅读说明

- 以 `@magustek/framework-ui` 的 `Mg*` 组件优先；当 `framework-ui` 无对应能力时，再使用 Element Plus 或自定义组件。
- 模板中统一使用 kebab-case 书写属性与事件（例如 `page-size`、`paging-change`）；脚本侧变量/方法使用 camelCase（例如 `pageSize`、`loadPageData`）。
- 以 `references/*` 与 `SKILL.md` 为主要来源；若其他文档与其冲突，以本文件约定为准并在维护时统一修正。

## 编码规范

### 命名规范

- 内部组件：使用 `Mg` 前缀，与组件库一致
- Element Plus：使用 `el-` 前缀（或自动导入时使用 `ElXxx`）
- 自定义组件：PascalCase，与文件名一致

```vue
<template>
  <MgTable :data="users" />
  <MgButton type="primary">提交</MgButton>

  <el-input v-model="username" />
  <ElInput v-model="username" />

  <UserProfile :user="currentUser" />
</template>
```

### 模板属性与事件命名

Vue 模板里属性与事件采用 kebab-case 书写（更符合 HTML 风格，也避免阅读分歧）。

| 语义 | 模板写法 | 脚本变量/方法 |
| --- | --- | --- |
| 当前页 | `:current-page` | `currentPage` |
| 每页条数 | `:page-size` | `pageSize` |
| 分页变化 | `@paging-change` | `loadPageData` |

### 类型安全

业务模型建议集中在 `types/` 维护，并在组件 props/emits 中显式约束。

```ts
export interface User {
  id: number
  username: string
  email: string
  role: 'admin' | 'user' | 'guest'
  status: 'active' | 'inactive' | 'pending'
  createdAt: Date
  updatedAt: Date
}

export interface UserForm {
  username: string
  email: string
  role: User['role']
  password?: string
}
```

```vue
<script setup lang="ts">
interface Props {
  user: User
  editable?: boolean
  onSave?: (user: User) => void
}

defineProps<Props>()
</script>
```

```vue
<script setup lang="ts">
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'submit', formData: UserForm): void
  (e: 'cancel'): void
}>()
</script>
```

## 组件使用最佳实践

### MgTable

#### 页面/容器满高（避免底部空白）

当页面由表格和其他元素（标题/搜索表单/工具栏）组成时，必须保证容器填满主内容区，且表格能够自动撑满剩余垂直空间。这适用于普通的块级元素（如 `div`）或自定义布局组件。

推荐方案是利用 Flex 布局的弹性特性：

1. **父容器**：设置为 `flex` 纵向布局，并给予 `height: 100%`。
2. **非表格区域**（标题、表单）：保持自然高度或固定高度。
3. **表格区域**：设置为 `flex: 1; min-height: 0;`，确保在内容较少时也能占据剩余空间。

```vue
<template>
  <div class="page-container">
    <!-- 1. 标题/页头区域 -->
    <div class="page-header">
      <h2>用户管理</h2>
    </div>

    <!-- 2. 搜索表单区域 -->
    <el-form class="search-form" :inline="true">
      <el-form-item label="用户名">
        <el-input v-model="query.name" />
      </el-form-item>
      <MgButton type="primary">查询</MgButton>
    </el-form>

    <!-- 3. 核心表格区域 (撑满剩余空间) -->
    <div class="table-wrapper">
      <MgTable :data="pageData" :loading="loading" height="100%">
        <!-- 列定义 -->
      </MgTable>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 16px;
  box-sizing: border-box;

  .page-header {
    margin-bottom: 16px;
    flex-shrink: 0; // 防止标题被压缩
  }

  .search-form {
    margin-bottom: 16px;
    flex-shrink: 0; // 防止表单被压缩
  }

  .table-wrapper {
    flex: 1;      // 占据剩余全部空间
    min-height: 0; // 关键：允许内容溢出滚动而不撑大容器
    
    :deep(.mg-table-content) {
      height: 100%;
    }
  }
}
</style>
```

**通用 CSS 链路 (AdminLayout 层级建议):**

为了减少每个页面的样板代码，建议在全局或布局组件中预设链路：

```css
/* 确保主区域填满 */
.admin-main {
  height: 100%;
  overflow: hidden;
}

/* 容器通用满高类 */
.full-height-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.flex-main-content {
  flex: 1;
  min-height: 0;
}
```

#### 前端分页 vs 后端分页

数据量小且可一次性拉取时用前端分页；数据量大或需要条件筛选时用后端分页。

```vue
<template>
  <MgTable :data="allData" :page-size="20" />

  <MgTable
    :data="pageData"
    :total="totalCount"
    v-model:current-page="currentPage"
    v-model:page-size="pageSize"
    @paging-change="loadPageData"
  />
</template>
```

#### 请求与分页单一可信源

后端分页时，页面内只保留一份 `currentPage` / `pageSize` 状态，并由 `@paging-change` 触发请求刷新列表，避免“状态多份维护导致页码错乱”。

```ts
const currentPage = ref(1)
const pageSize = ref(20)
const totalCount = ref(0)
const loading = ref(false)

const loadPageData = async () => {
  loading.value = true
  try {
    const { list, total } = await fetchUsers({ page: currentPage.value, pageSize: pageSize.value })
    pageData.value = list
    totalCount.value = total
  } finally {
    loading.value = false
  }
}
```

#### loading 与空态

列表页需要显式管理加载态，并将请求中的 `loading` 贯穿到页面交互（例如工具栏按钮、表格加载态、弹窗提交）。

```vue
<template>
  <MgTable :data="pageData" :loading="loading" />
</template>
```

#### 表格列定义

```vue
<template>
  <MgTable :data="users">
    <el-table-column type="selection" width="55" />
    <el-table-column prop="username" label="用户名" width="120" />
    <el-table-column prop="status" label="状态" width="100">
      <template #default="{ row }">
        <el-tag :type="row.status === 'active' ? 'success' : 'info'">
          {{ row.status === 'active' ? '激活' : '禁用' }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="200" fixed="right">
      <template #default="{ row }">
        <MgButton type="primary" size="small" @click="editUser(row)">编辑</MgButton>
        <MgButton type="danger" size="small" @click="deleteUser(row)">删除</MgButton>
      </template>
    </el-table-column>
  </MgTable>
</template>
```

### MgDialog

#### 表单对话框模式

对话框建议固定三段式：打开（回填/重置）→ 提交（校验/请求/关闭）→ 关闭（reset + 清理状态）。

```vue
<template>
  <MgDialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '新增用户'" width="500px" :before-close="handleBeforeClose">
    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px" status-icon>
      <el-form-item prop="username" label="用户名">
        <el-input v-model="formData.username" />
      </el-form-item>
    </el-form>

    <template #footer>
      <MgButton :disabled="submitting" @click="dialogVisible = false">取消</MgButton>
      <MgButton type="primary" :loading="submitting" @click="handleSubmit">{{ isEdit ? '更新' : '创建' }}</MgButton>
    </template>
  </MgDialog>
</template>
```

未保存更改时关闭确认：

```ts
const dialogVisible = ref(false)

const handleBeforeClose = (done: () => void) => {
  if (!hasUnsavedChanges()) {
    done()
    return
  }

  ElMessageBox.confirm('有未保存的更改，确定要关闭吗？').then(done)
}
```

### 表单

#### 表单验证

```vue
<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'

const formRef = ref<FormInstance>()

const formData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (_, value) => (value !== formData.password ? Promise.reject(new Error('两次输入密码不一致')) : Promise.resolve()),
      trigger: 'blur',
    },
  ],
}

const handleSubmit = async () => {
  if (!formRef.value) return
  const valid = await formRef.value.validate()
  if (!valid) return
  await submitForm()
}
</script>
```

#### 表单重置

重置表单时优先使用 `resetFields()`，并将 reactive 对象回到默认值，确保再次打开对话框不“残留上次内容”。

```ts
const resetForm = () => {
  formRef.value?.resetFields()
  Object.assign(formData, {
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  })
}
```

### 可访问性

- 输入类组件提供明确的 `label`（`el-form-item label`），按钮文案避免只用图标表达语义。
- 弹窗的默认焦点落点明确（打开后聚焦第一个输入），并保证键盘可完成主要流程（Tab/Enter/Esc）。

