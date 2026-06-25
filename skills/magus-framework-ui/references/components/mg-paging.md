# MgPaging

分页器组件，基于 Element Plus `ElPagination` 封装。

用于：列表分页、表格分页导航。

---

## Usage

```vue
<MgPaging
  :total="100"
  v-model:current-page="currentPage"
  v-model:page-size="pageSize"
  @change="handleChange"
/>
```

```ts
import { ref } from 'vue'
import { MgPaging } from '@magustek/framework-ui'

const currentPage = ref(1)
const pageSize = ref(20)

const handleChange = (page: number, size: number) => {
  console.log('分页改变:', page, size)
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| total | `number` | 是 | `0` | 数据总数 |
| currentPage | `number` | 否 | `1` | 当前页码 |
| pageSize | `number` | 否 | `20` | 每页条数 |
| pageSizes | `number[]` | 否 | `[20, 50, 100, 200]` | 每页条数选项 |
| layout | `string` | 否 | `'sizes, prev, pager, next, jumper'` | 分页器布局 |
| showTip | `boolean` | 否 | `true` | 是否显示提示信息 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:currentPage | `number` | 当前页码改变时触发 |
| update:pageSize | `number` | 每页条数改变时触发 |
| change | `(page: number, size: number)` | 分页改变时触发 |

---

## AI Usage Rules

1. `total` 为必填项，决定总页数。
2. 分页改变时同时触发 `change` 和 `update:currentPage` / `update:pageSize`。
3. `layout` 支持 Element Plus 分页布局字符串，如 `'total, prev, pager, next, jumper'`。
