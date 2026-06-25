# File-Based Routing

此文件只描述文件式路由的目录到路由映射、页面命名和路由元信息规则。手写路由项目应遵循目标项目现有 router 表。

项目使用 Vue Router 5，并通过 `vue-router/vite` 集成文件式路由与自动生成。页面组件位于 `src/pages`。

## Vite 插件硬要求

文件式路由项目的 `vite.config.ts` 必须同时包含以下配置：

- `import VueRouter from 'vue-router/vite'`
- `import { VueRouterAutoImports } from 'vue-router/unplugin'`
- `plugins` 中注册 `VueRouter(...)`，以 `src/pages` 为页面目录；微前端部署下 `VITE_APP_BASE` 必须非空。
- `AutoImport({ imports: [...] })` 中包含 `VueRouterAutoImports`

缺少任一项都会导致 `src/pages` 文件式路由、`definePage` 或路由类型自动导入不完整。新建前端骨架时不得因为业务页面较少而退回手写 `src/router/*.ts` 业务路由表；只有目标项目已存在手写路由模式时，增量页面才跟随目标项目既有模式。

## 基本路由

文件式路由页面按设计阶段 `menuPageContext.frontend.menuFilePath` 落位，并生成对应 `routePath`。基础映射如下：

- `src/pages/index.vue` -> `/`
- `src/pages/resource/index.vue` -> `/resource`
- `src/pages/resource/page.vue` -> `/resource/page`

若首页就是应用入口页，则使用 `src/pages/index.vue`，其内部 `routePath` 为 `/`。

## path 前缀与相对目录

必须区分以下路径：

- `VITE_APP_BASE`：Vite 部署前缀值，例如 `system`、`menu`。
- `pageRelativeRoute`：`src/pages` 下的相对页面路径，例如 `project`、`role`、`user`；根入口为空。
- `routePath`：Vue Router 内部业务路径，由 `pageRelativeRoute` 生成，例如 `/project`、`/role`、`/user`、`/`。
- `menuFilePath`：菜单页面文件路径，例如 `src/pages/project/index.vue`。
- `publicAccessPath`：浏览器公开访问路径，等于 `join("/", VITE_APP_BASE, routePath)`。

默认配置示例：

组合规则：`pageRelativeRoute=project -> src/pages/project/index.vue -> routePath=/project`；`pageRelativeRoute="" -> src/pages/index.vue -> routePath=/`。

生成页面后必须检查 `menuFilePath`、`routePath` 和 `publicAccessPath` 与设计阶段 `menuPageContext.frontend` 一致。

## Layout 菜单同步

项目启用 `VITE_APP_FRAME` 微前端开发布局时，业务功能入口路由必须同步到开发期菜单配置。菜单 path 使用文件式路由生成的 `route.path`，不使用文件路径、路由组名或部署前缀。

文件式路由页面默认通过 `definePage({ name, meta: { menu } })` 声明 layout 菜单元信息。普通业务菜单不得在 `meta.menu` 中手写 `path`；layout 必须从 `router.getRoutes()` 提取 `route.meta.menu`，用最终 `route.path` 补齐菜单 `path`，再用 `parentNodeId` 组装树。外链菜单或非路由菜单是例外，必须显式标记为外链并说明来源。

```vue
<script setup lang="ts">
defineOptions({ name: 'IndexPage' })

definePage({
  name: 'IndexPage',
  meta: {
    menu: {
      nodeId: 'home',
      text: '首页',
      icon: 'HomeFilled',
      order: 1,
      hidden: false,
    },
  },
})
</script>
```

`hidden` 必须显式判断并写入：

- 列表页、首页、仪表盘、独立配置页，且可从菜单直接访问时，`hidden: false`。
- 路径包含动态参数时，默认 `hidden: true`。
- 页面名称或路径语义为 `add/create/edit/update/detail/view` 时，默认 `hidden: true`。
- 业务流程操作页只能从按钮或行操作进入时，`hidden: true`。
- 用户或设计明确要求作为菜单展示时，即使是子页面也可 `hidden: false`，但路径不得依赖动态参数。
- `hidden: true` 的页面必须设置 `parentNodeId`。

layout 菜单提取示例：

```ts
type LayoutMenu = {
  nodeId: string
  text: string
  path?: string
  icon?: string
  order?: number
  hidden: boolean
  parentNodeId?: string
  children?: LayoutMenu[]
}

const flatMenus = router.getRoutes()
  .filter((route) => route.meta?.menu)
  .map((route) => ({
    ...route.meta.menu,
    path: route.path,
    children: [],
  })) as LayoutMenu[]

const visibleMenus = flatMenus.filter((item) => !item.hidden)
const menuMap = new Map(visibleMenus.map((item) => [item.nodeId, item]))
const menuTree: LayoutMenu[] = []

for (const item of visibleMenus) {
  if (item.parentNodeId && menuMap.has(item.parentNodeId)) {
    menuMap.get(item.parentNodeId)!.children!.push(item)
  } else {
    menuTree.push(item)
  }
}

const sortMenus = (menus: LayoutMenu[]) => {
  menus.sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
  menus.forEach((item) => sortMenus(item.children ?? []))
}

sortMenus(menuTree)
```

文件式路由页面存在但 layout 菜单 path 不匹配时，必须先修正菜单映射再声明页面可用。

## 运行访问路径

运行或浏览器调试时，实际访问路径由 `VITE_APP_BASE` 微应用部署前缀和内部 `routePath` 共同决定：`publicAccessPath=join("/", VITE_APP_BASE, routePath)`。微前端部署下 `VITE_APP_BASE` 禁止为空；即使内部 `routePath=/`，浏览器访问路径仍必须包含 `VITE_APP_BASE`。

## 菜单页面路径

涉及菜单页面或 `@AppGroupInfo` 时，前端必须使用设计阶段 `menuPageContext.common` 和 `menuPageContext.frontend`。文件式路由菜单页面消费 `frontend.VITE_APP_BASE`、`frontend.pageRelativeRoute`、`frontend.routePath`、`frontend.menuFilePath` 和可选 `frontend.publicAccessPath`。

拆分结果必须满足：`frontend.routePath = common.finalMenuPath`。入口页的相对路由为空时使用 `src/pages/index.vue`；多级相对路由按目录层级落位。后端只消费 `backend.appGroupInfoPage`。

必须验证 `frontend.routePath`、`route.path`、layout 菜单 path 和 `common.finalMenuPath` 一致。此规则只约束菜单页面；新增、编辑、详情等非菜单页面按已确认路由需求选择相对文件结构。

## 动态路由

- 参数：`src/pages/users/[id].vue` -> `/users/:id`
- 可选参数：`src/pages/users/[[id]].vue` -> `/users/:id?`
- 捕获所有：`src/pages/[...path].vue` -> `/:path(.*)`

## 嵌套路由

通过定义一个与目录同名的 `.vue` 文件实现嵌套路由。

```text
src/pages/
├── users/
│   └── index.vue
└── users.vue
```

对应路由：

```ts
const routes = [
  {
    path: '/users',
    component: () => import('src/pages/users.vue'),
    children: [
      { path: '', component: () => import('src/pages/users/index.vue') },
    ],
  },
]
```

## 业务入口目录

生成用户可访问的业务一级入口时，按 `menuPageContext.frontend.menuFilePath` 落位。页面跳转使用 `common.finalMenuPath` 对应的内部业务 path；浏览器访问使用 `publicAccessPath`。后端只消费 `backend.appGroupInfoPage`。

正确示例：

```text
src/pages/
├── index.vue       # routePath=/
├── page.vue        # routePath=/page
└── detail.vue      # routePath=/detail
```

对应路由结构应为：

```text
/
├── '' -> RouteIndexPage
├── page -> RoutePage
└── detail -> RouteDetailPage
```

生成后必须验证 `VITE_APP_BASE` 对应部署入口和用户指定业务入口均可访问，不出现空白页；同时检查 `menuFilePath`、`routePath`、页面跳转和 `publicAccessPath` 与设计阶段上下文一致。

## 命名视图

文件 `src/pages/index@aux.vue` 对应路由配置：

```ts
{
  path: '/',
  components: {
    aux: () => import('src/pages/index@aux.vue'),
  },
}
```

## 页面命名

页面组件内部**必须**使用 `defineOptions` 定义 **PascalCase** 名称（即使是 `index.vue`）。

```vue
<script setup lang="ts">
defineOptions({ name: 'UserIndex' })
</script>
```

## 路由元信息

页面内必须使用 `definePage` 设置稳定路由 `name`。路由页面涉及 layout 菜单时，还必须生成 `meta.menu`；不涉及菜单展示的页面也应通过 `definePage` 显式声明 `name`，便于命名跳转和类型生成。

```vue
<script setup lang="ts">
defineOptions({ name: 'PascalCaseName' })
definePage({
  name: 'PascalCaseName',
  meta: {
    menu: {
      nodeId: 'pascal-case',
      text: '菜单名称',
      order: 10,
      hidden: false,
    },
  },
})
</script>
```

规则：

- pages 目录下所有页面默认布局为 `default`，无需重复设置。
- 路由页面默认生成 `definePage({ name })`；需要改变布局、设置 alias、redirect 或菜单元信息时，在同一个 `definePage` 中扩展。
- `defineOptions({ name })` 只定义 Vue 组件名，不会定义 route name；不得把组件名当作命名路由跳转依据。
- 使用 `router.push({ name: 'XxxAdd' })`、`router.push({ name: 'XxxEdit' })` 等命名跳转时，目标页面必须通过 `definePage({ name: '...' })` 或目标项目真实路由表声明完全一致的 route name。
- 新增、编辑、详情按钮生成后必须检查“点击事件 -> 跳转方法 -> 目标路由”闭环，确认目标 route name 或 path 实际存在。
- 多级目录需要改变布局时，创建与文件夹同名的 `.vue` 文件，并在该文件中设置。

## 页面级公共目录

`src/pages` 下的 `components`、`utils`、`composable` 目录不生成路由，用于页面级公共组件、工具函数和组合式函数。

全局通用组件、工具函数、组合式函数应放在 `src/components`、`src/utils`、`src/composable`。

## 边界

- 不在本文件定义页面 UI 范式，见 `module-development-standard.md`。
- 不在本文件定义权限或菜单登记注解。
- 手写路由、微前端主路由和既有项目路由以目标项目现有代码为准。
