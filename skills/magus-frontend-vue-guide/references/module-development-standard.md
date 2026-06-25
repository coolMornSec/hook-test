# Module Development Standard

本 reference 只描述 Magus Vue 业务模块的落地流程、页面分层、状态交互和生成顺序。API、权限、字典、主题、i18n、路由和组件 API 细节分别由对应 reference 负责。

## 使用前提

- 目标项目已经存在前端骨架或同类模块。
- 已确认业务范围、接口契约、权限码、字典 code、主题/i18n 策略和验收点。
- 先识别目标项目真实目录和既有同类模块，再决定文件落位。

## 模块目录

文件式路由项目优先采用页面内聚结构：

```text
src/
├── api/
│   └── [module]/
│       ├── index.ts
│       └── types.ts
├── lang/
├── pages/
│   └── [relative-module]/
│       ├── components/
│       │   └── XxxForm.vue
│       ├── composable/
│       │   └── useXxx.ts
│       ├── types/
│       │   ├── domain.ts
│       │   ├── form.ts
│       │   └── view.ts
│       ├── mapper.ts
│       ├── index.vue
│       ├── add.vue
│       ├── edit/[id].vue
│       └── detail/[id].vue
├── router/
├── styles/
└── types/      # 仅跨模块共享基础类型、工具类型和全局声明
```

当 `[relative-module]` 是 `@AppGroupInfo` 对应的菜单页面时，由 `frontend.pageRelativeRoute` 决定 `src/pages` 目录。必须验证 `common.finalMenuPath=frontend.routePath=backend.appGroupInfoPage`。

手写路由或老 Magus 微前端项目按目标项目已有 `src/view`、`router`、`types`、`lang` 分层落位，不强行迁移到 `src/pages`。

## 页面分层

列表页：

- 外层保持满高布局，形成 `h-full`、`min-h-0`、`overflow-hidden` 链路。
- 标准组合为 `MgLayout`，`#header` 放 `MgSearch`，`#main` 放 `MgToolbar` 和 `MgTable`。
- 搜索触发时重置 `page = 1`；清空筛选后状态可预期。
- 服务端分页由 `MgTable` 绑定分页状态并监听分页变化重新请求。
- 批量按钮绑定禁用态；请求成功后清空 selection。
- 行操作必须阻止冒泡，固定右侧并设置明确宽度。

新增/编辑/详情页：

- 新增、编辑、详情无论字段多与少，均默认推荐使用独立路由页，不塞进弹窗。
- 使用 `MgBackWrap` 或目标项目已有返回壳提供标题和返回。
- 列表页新增、编辑、详情按钮必须绑定真实点击处理，并能跳转到已存在的目标路由；使用命名路由时，目标 route name 必须由真实路由表或文件式路由页面的 `definePage` 声明。
- 当新增、编辑、详情复用，或表单字段超过 3 个时，默认抽 `components/XxxForm.vue`。
- 表单组件只负责字段、校验、默认值、reset、submit/cancel 事件。
- 页面负责加载详情、调用 API、处理成功反馈、返回或关闭页签。
- 详情页与新增/编辑字段结构高度一致时，可复用 `XxxForm` 的只读模式或同目录详情组件；展示结构明显不同则抽独立详情展示组件，不强行复用表单。
- 大表单可用 `el-tabs` 分组，但保持同一个提交出口。
- 独立新增或编辑页默认使用 `MgBackWrap` 或等价返回壳，表单必须具备 `prop`、规则和提交前校验闭环。

弹窗：

- 弹窗或确认框用于删除确认、辅助选择、非表单信息展示、导入导出配置等轻量交互。
- 新增、编辑、详情不默认使用弹窗；只有需求或设计明确指定为轻量内嵌流程时才允许例外，并必须记录依据。
- 弹窗内存在表单时，必须处理打开重置、关闭清理、字段规则、`formRef.validate()`、提交 loading 和未保存变更风险。
- `MgLayout` 页面中，`el-dialog`、`el-drawer` 和全屏浮层不放在 `MgLayout` 默认 slot 内，应放在 `MgLayout` 同级；wujie / shadow DOM 场景下必须显式使用子应用内挂载策略。
- wujie 子应用中，`el-dialog` 必须设置 `:append-to-body="false"` 和 `:modal-append-to-body="false"`；`el-drawer`、`el-popover`、`el-tooltip` 同样需要 `:append-to-body="false"` 或等价约束。

## 状态与交互

列表状态：

- `loading`
- `empty`
- `error`
- `selection`
- `total`
- `page`
- `size`

表单状态：

- `submitting`
- `dirty`
- `disabled`
- `defaultValue`
- `validation`
- `serverError`

交互规则：

- 删除、取消授权、重置密码、状态切换等影响数据的动作必须二次确认。
- 成功后刷新列表并清空选择；失败时保留当前数据和选择状态。
- 列表页、看板页、图表页首屏接口必须 `catch`，并提供 loading、空态或错误态；不得让接口失败表现为空白页。
- 缓存页签刷新使用目标项目已有 `onActivated`、`onShow` 或 `watchInComponent` 模式。
- 返回优先使用目标项目已有页签关闭/返回工具；没有时使用 router 返回并说明。

## Composable 设计

- 每个 composable 按业务状态的生命周期、职责边界、副作用来源和可测试性划分，不得混用、不得过度抽象。
- 返回值超过 10 个时，必须拆分为多个 composable 或返回对象分组。
- composable 内部不直接调用 `ElMessage`、`ElMessageBox` 或 `router.push`；这些属于 UI 层职责，应由页面组件处理。
- composable 不得持有组件 ref，如 `tableRef`；不得依赖 DOM。
- 命名使用 `use{Domain}{Action}`，如 `useMenuTree`、`useMenuList`、`useMenuForm`。

## 样式

- 后台页面应安静、紧凑、可扫描，不做营销 hero、装饰渐变、大卡片套卡片。
- 搜索、工具栏、表格和分页必须有稳定高度与滚动边界。
- Tailwind 项目写 Tailwind class；UnoCSS 项目写属性模式；SCSS 中优先 `@apply`。
- 新增模块样式默认 scoped；只为布局、尺寸、状态和局部细节写样式。
- 列表、tab页、卡片等布局容器，都不允许出现大量底部或侧边空白
- 模板中每层 DOM 容器必须承担可追溯的布局职责，禁止出现无 class、无 style、无指令、无语义角色的匿名空包装容器。
- 页面内容区禁止出现静态解释性文本标签。页面内只放置业务数据和操作控件。反例：`<p>一级菜单</p>`、`<span>当前展示{{xxx}}信息</span>`。

## 生成顺序

1. 建立需求到代码映射表。
2. 按 `type-definition-standard.md` 创建 API 契约类型、领域模型、展示模型、表单模型和必要 mapper。
3. 实现列表页或主页面。
4. 实现新增、编辑、详情页和复用组件。
5. 接入权限、字典、i18n、主题和边界状态。
6. 执行验证并编写交付说明。

验证新增、编辑、详情交互时，不能只检查按钮已渲染；必须检查点击处理已绑定、目标路由存在且跳转参数与目标页面读取方式一致。

批量迁移或重排 `.vue` 模板结构后，至少运行 SFC parse、`vue-tsc --noEmit` 或项目等价 typecheck；不得只用字符串搜索确认标签结构。

## 运行时风险

- 遇到运行时空白页，必须优先读取浏览器 console 的第一条真实错误和 network 中的首个失败请求，再提出修复假设。
- 不能把组件名大小写、import 或样式相似点当成根因完成；静态修复后若问题仍存在，必须回到 console / network / DOM 根因调查。
- wujie / shadow DOM / 多 Document 环境中，禁止依赖 `document.body` 定位或裸 `document.body.appendChild`；Teleport 目标必须在子应用内。
- 新建或修改 `main.ts` 且目标项目作为 wujie 子应用运行时，必须修补 `document.adoptedStyleSheets` setter，避免跨 Document 共享 constructed stylesheet。
- 禁止直接使用会在模块加载阶段写入 `document.adoptedStyleSheets` 的组件库包装层。若出现 `Sharing constructed stylesheets in multiple documents is not allowed`，优先替换为本地组件封装或普通 `<style>` 注入方案。

## 边界

- 不定义接口写法，见 `api-permission-dictionary.md`。
- 不定义类型落位、命名和 mapper 细则，见 `type-definition-standard.md`。
- 不定义主题/i18n 细节，见 `i18n-theme.md`。
- 不定义路由语法，见 `file-based-routing.md`。
- 不定义组件 props/events/slots，见 `magus-framework-ui.md` 和对应组件 reference。
