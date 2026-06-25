# MgLayout

企业级布局组件，支持侧边栏、头部、主内容、底部的完整页面布局。主内容区域自动添加滚动条。

用于：管理后台布局、左右分栏布局、带侧边栏的页面。

---

## Usage

```vue
<MgLayout aside-width="280px" gap="16px">
  <template #aside>
    <el-menu :default-active="activeMenu" @select="handleMenuSelect">
      <el-menu-item index="users">用户管理</el-menu-item>
      <el-menu-item index="roles">角色管理</el-menu-item>
    </el-menu>
  </template>
  <template #header>
    <div class="navbar">欢迎，{{ userName }}</div>
  </template>
  <template #main>
    <router-view />
  </template>
  <template #footer>
    <div class="footer">© 2026 Company</div>
  </template>
</MgLayout>
```

```ts
import { ref } from 'vue'
import { MgLayout } from '@magustek/framework-ui'

const activeMenu = ref('users')
const userName = ref('Admin')

const handleMenuSelect = (index: string) => {
  console.log('选择菜单:', index)
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| asideWidth | `string` | 否 | `'300px'` | 侧边栏宽度 |
| gap | `string` | 否 | `'16px'` | 各区域间距 |

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| aside | `void` | 左侧侧边栏内容，不提供则不显示侧边栏 |
| header | `void` | 顶部头部内容 |
| main | `void` | 主内容区域（必需） |
| footer | `void` | 底部页脚内容 |

---

## Types

```ts
export interface MgLayoutProps {
  asideWidth?: string
  gap?: string
}
```

---

## AI Usage Rules

1. `main` 插槽是必需的，其他插槽均可选。
2. 组件默认填满父容器，确保父容器有明确的高度。
3. 主内容区域自动添加滚动条。
4. 侧边栏宽度支持 CSS 单位（`px`、`%`、`em` 等）。
5. 如果不提供 `aside` 插槽，侧边栏不渲染，布局变为顶部+主内容+底部三栏。
