# MgSearch

搜索框组件，基于 Element Plus `ElInput` 封装，提供搜索按钮和清空功能。

用于：列表搜索、关键词过滤。

---

## Usage

```vue
<MgSearch
  showMore
  isExpand
  :contentGrowth="true"
  :showSearchIcon="true"
  :labelWidth="120"
  placeholder="输入搜索关键词"
  @search="handleSearch"
>
  <template #search>
    <el-form-item label="用户名">
      <el-input v-model="searchForm.username" />
    </el-form-item>
    <el-form-item label="邮箱">
      <el-input v-model="searchForm.email" />
    </el-form-item>
  </template>
  <template #more>
    <el-form-item label="手机号">
      <el-input v-model="searchForm.phone" />
    </el-form-item>
  </template>
  <template #buttons>
    <el-button type="primary" @click="handleSearch">搜索</el-button>
    <el-button @click="handleReset">重置</el-button>
  </template>
</MgSearch>
```

```ts
import { reactive } from 'vue'
const searchForm = reactive({
  username: '',
  email: '',
  phone: '',
})

const handleSearch = (event: any) => {
  console.log('search', searchForm)
}
const handleReset = () => {
  searchForm.username = ''
  searchForm.email = ''
  searchForm.phone = ''
}
```

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| showMore | `boolean` | 否 | `''` | 展示更多按钮 |
| showSearchIcon | `boolean` | 否 | `'搜索'` | 占位符 |
| labelWidth | `number` | 否 | 100 | 标签宽度 |
| showButtons | `boolean` | 否 | `true` | 是否显示按钮组 |
| contentGrowth | `boolean` | 否 | `true` | 内容自适应 |
| isExpand | `boolean` | 否 | `false` | 是否展开表单 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| search | `string` | 点击搜索按钮时触发 |
