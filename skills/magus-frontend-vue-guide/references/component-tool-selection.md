# Component and Tool Selection

此文件只描述组件库、业务组件、工具库、图标和自动导入的选择规则。组件 API 细节以 `magus-framework-ui.md` 指向的事实源为准。

## 组件优先级

1. `@magustek/framework-ui`：通用 `Mg*` 组件。
2. `@magustek/framework-biz-ui`：业务选择、返回壳、上传、字典、资源等。
3. Element Plus：Magus 没有覆盖或需要原生能力时使用。
4. 自定义组件：只有组件库无法表达业务且复用价值明确时创建。

回退到 Element Plus 或自定义组件时，在交付说明中写清原因。

## 常用场景

| 场景 | 优先组件 |
|---|---|
| 标准列表 | `MgLayout` + `MgSearch` + `MgToolbar` + `MgTable` |
| 简单 CRUD 列表 | `MgPageTable` 可作为快速组合 |
| 返回式表单/详情 | `MgBackWrap` |
| 局部弹窗 | `MgDialog` |
| 左树右表 | `MgLayout` + `MgTree` + `MgTable` |
| 表格分页 | `MgTable` 内置分页或 `MgPaging` |
| 日期时间 | `MgDatePicker` / `MgTimePicker` |
| 级联 | `MgCascader` |
| 图标选择/渲染 | `MgIconPicker` / `MgIcon` / `@magustek/icon-svg` |
| 用户/部门/职务/工作组 | `MgComplexSelect` |
| 菜单/资源授权 | `MgResourceSelect` |
| 文件上传 | `MgUpload` 或项目已有上传封装 |
| 字典 | `MgDict`、`useDicts` 或项目已有字典组件 |
| 图表 | wujie 子应用优先本地 `EchartsView` + `echarts/core`；非 wujie 场景按目标项目已有图表封装 |

使用具体 props、events、slots、methods 前必须读取 `magus-framework-ui.md` 指向的对应 component reference 或 Biz UI reference。

## 微前端组件兼容

- 无界 / wujie / shadow DOM / 多 Document 环境中，不直接引入会在模块加载阶段写入 `document.adoptedStyleSheets` 的第三方 Vue 组件包装层。
- 图表优先使用本地 `EchartsView` 管理 `echarts/core` 的 `init` / `dispose` / `resize`；必须使用 `vue-echarts` 或其他第三方 Vue 图表组件时，先检查是否依赖 `adoptedStyleSheets` 或 `document.body` Teleport。
- 浮层组件必须使用子应用内挂载策略；不裸用 `document.body.appendChild`。

## 工具库

- VueUse 优先：路由参数、query、debounce/throttle、事件监听、存储、剪贴板、窗口尺寸、异步状态等。
- es-toolkit 次之：对象裁剪、分组、去重、排序、深合并、谓词、Promise 并发等。
- 不新增 lodash-es；旧代码可保留，新增逻辑优先 VueUse/es-toolkit。
- 简单逻辑直接写在模块 composable；多个模块复用再提到项目级 `src/composable` 或 `src/utils`。

## 图标

- 优先项目已注册的 `@magustek/icon-svg` 或 Element Plus Icons。
- 按钮图标服务识别，不做装饰。
- 项目全局注册图标时模板可直接用组件；未注册时按需 import。

## 自动导入

先检查 `vite.config.ts` 的 `AutoImport` 和 `Components` resolvers：

- 已自动导入的 Vue、Pinia、Vue Router、Element Plus、VueUse、Magus 工具和组件不重复 import。
- 类型导入、局部组件、未注册图标和目标项目未覆盖的 API 可以显式 import。
- 不生成 `auto-imports.d.ts`、`components.d.ts`、`router-map.d.ts`；这些由工具链生成。

## 边界

- 不在本文件维护组件 API，避免与组件 reference 漂移。
- 不在本文件定义页面布局细节，见 `module-development-standard.md`。
- 不在本文件定义 API、权限或字典契约，见 `api-permission-dictionary.md`。
