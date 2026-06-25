---
name: magus-frontend-vue-guide
description: Use when Magus Vue 3 business modules after a frontend skeleton already exists, covering requirements analysis, functional design, implementation planning, document review, code implementation, API files, type definitions, permissions, dictionaries, i18n, theme adaptation, file-based routes, component selection, UI style, and delivery verification.
---

# Magus Frontend Vue Guide

## 定位

本技能用于“前端骨架初始化之后”的 Magus Vue 3 业务模块全流程规范，包括需求确认、功能设计、实施计划、文档评审、代码实现和交付验证。它负责约束已有 Magus 前端项目中的页面、组件、API、类型定义、权限码、字典、路由、主题、国际化和验证要求。

## 输入与输出边界

- 适用条件：已有前端骨架上的页面、组件、API、路由、权限展示、字典、i18n、主题和微前端兼容开发。
- 必要输入：目标项目、页面与交互范围、API/DTO 契约、菜单路由、权限与字典事实源、视觉方向。
- 标准输出：业务页面与组件、API/类型、路由菜单、i18n/样式实现和 typecheck/build 证据。
- 不负责：初始化新骨架、设计新权限模型、虚构接口字段或用 mock 掩盖缺失契约。

本技能不负责：

- 初始化前端骨架、创建新项目或重写全局架构。
- 设计新的权限模型、权限码体系、角色授权流程或菜单权限方案。
- 凭空补充字段、接口、权限码、字典 code、主题 token、语言 key、页面流程或 mock 数据。
- 用模板示例替代目标项目的真实契约。

## 输入门禁

写代码前必须先确认以下事实。已有需求、设计、计划、接口契约或用户记录中已经明确的，直接使用；缺失时必须先提问并等待回答。

| 事实 | 必须确认的内容 |
|---|---|
| 业务范围 | 模块名称、页面范围、字段、操作、状态、验收点 |
| API | 后端 `serviceName`/`spring.application.name`、网关路由前缀、Controller 实际 URL、GET/POST 方法、Req/Rsp DTO、字段名、类型、必填项、分页请求字段、分页响应字段、错误处理 |
| 权限 | 按钮、批量操作、导出、删除、启停、授权等敏感动作的权限码 |
| 字典 | 字典 code、label/value 字段、状态色、枚举来源 |
| 路由 | 目标项目使用文件式路由还是手写路由；是否启用 layout；设计阶段 `menuPageContext.frontend` 中的 `VITE_APP_BASE`、`pageRelativeRoute`、`routePath`、`menuFilePath`、列表、新增、编辑、详情相对路径和公开访问路径 |
| 菜单页面 | 涉及菜单页面或 `@AppGroupInfo` 时，读取设计阶段 `menuPageContext.common` 和 `menuPageContext.frontend`；必须满足 `common.finalMenuPath=frontend.routePath=backend.appGroupInfoPage` |
| 类型策略 | API 契约、生成类型、领域模型、展示模型、表单模型、组件私有类型、共享基础类型的归属和落位；缺失时先按 `references/type-definition-standard.md` 判定，不得默认放入 `src/types/` |
| 组件 | 目标项目已有同类模块、Magus 组件、Biz 组件或 Element Plus 回退原因 |
| i18n | `useI18n` 是否启用、已有语言集合、模块命名空间 |
| 主题 | `requiresCustomTheme` 是否启用、主题来源或明确 token |

主题和 i18n 是硬开关：

- `requiresCustomTheme = false`：沿用项目现有主题，只写布局、尺寸、状态和局部修正样式。
- `requiresCustomTheme = true`：只使用已确认的 `themeSource` 或 `themeTokens`；缺 token 时继续确认。
- `useI18n = false`：允许使用清晰中文业务文案，不创建孤立语言包。
- `useI18n = true`：所有用户可见文案、校验和消息都必须接入 i18n。
- 目标项目已经强制 i18n 时，项目规范优先；若用户要求不使用，回到确认阶段处理冲突。

## Reference 导航

详细规范只维护在 references 中。使用本技能时必须按任务命中的领域读取对应 reference；不得只读取 `SKILL.md` 后直接生成代码。阶段输出必须记录已读取的 reference 及适用结论。

| 任务 | 必读 |
|---|---|
| 模块结构、页面分层、状态交互、生成顺序 | `references/module-development-standard.md` |
| API、权限、字典、确认弹窗 | `references/api-permission-dictionary.md` |
| 类型定义位置、命名、职责拆分、mapper 和类型检查 | `references/type-definition-standard.md` |
| i18n 增量、语言合并、主题开关、主题验证 | `references/i18n-theme.md` |
| 文件式路由、动态路由、`definePage`、页面级公共目录 | `references/file-based-routing.md` |
| 组件库和工具库选择、自动导入、图标 | `references/component-tool-selection.md` |
| 默认后台技术栈、目录和视觉基线 | `references/magus-admin-ui-baseline.md` |
| `useAxios`、字典、locale、store、页签等 core 能力 | `references/magus-framework-core.md` |
| 页签返回、keep-alive 显示、下载、模板下载 | `references/magus-framework-biz-utils.md` |
| Framework UI 组件事实入口 | `references/magus-framework-ui.md` |

模板只用于理解默认模式，复制前必须替换所有占位符、接口、权限码、字段、路由名和语言文案：

- 列表页：`templates/index.vue`
- 新增页：`templates/add.vue`
- 编辑页：`templates/edit/[id].vue`
- 复用表单：`templates/components/XxxForm.vue`
- 默认导出 API：`templates/api/index.ts`
- API 类型：`templates/api/types.ts`
- 组合式 API：`templates/api-composable/useXxxApi.ts`
- 组合式 API 类型：`templates/api-composable/types.ts`
- 模块 composable：`templates/composable/useXxx.ts`

## 开发流程

1. 建立“需求到代码映射表”：页面、字段、接口、权限、字典、状态、校验、交互、i18n、主题、验收点。
2. 识别目标项目真实模式：目录、路由、API 组织、自动导入、样式体系、i18n 合并、主题变量、同类模块写法。
3. 按 reference 实现 API/DTO、领域模型、展示模型、表单模型、页面、组件、路由、权限、字典、i18n 和样式。
4. 对照映射表自检，删除文档外字段、按钮、页面、接口、权限码、字典 code、主题 token 和语言 key。
5. 运行最相关验证：类型检查、构建、lint/test、浏览器烟测、i18n 切换、主题检查。

## 硬边界

- API、权限、字典细则只按 `api-permission-dictionary.md` 执行。
- 类型定义位置、命名、职责拆分和 mapper 只按 `type-definition-standard.md` 执行；不得默认把业务类型放入 `src/types/`。
- 前端最终发出的后端业务请求必须包含网关路由段：`/api/{spring.application.name}/{controllerPath}`；使用 `useAxios()` 且项目默认已注入 `/api` 时，API 模块 URL 仍必须以 `/{spring.application.name}` 开头。
- 前端请求方法、参数位置、路径和字段名必须严格匹配后端 Controller / DTO 契约。API 路径必须以实际 Controller 类级 `@RequestMapping` + 方法级 `@GetMapping` / `@PostMapping` 路径为准；不得按接口名称、RESTful 习惯或 kebab-case 自行推演。`GET + @RequestParam` 必须生成平铺查询参数，不得包装成会产生 `params[page]`、`params[size]` 的嵌套对象，也不得生成后端未声明的通用搜索字段。
- 生成前端请求或响应类型前，必须先读取实际后端 Req/Rsp DTO；后端代码尚未生成时，以已确认的 `apiContractContext` 为临时唯一事实源，并在开发后契约复核中再次对照实际 DTO。字段名、类型、必填项、枚举、分页字段和错误结构不得由页面文案或交互语义推演。
- 使用 `useAxios` 或其他返回响应式引用的请求封装时，必须先按其真实 TypeScript 返回类型显式解包，再访问响应字段。优先使用泛型、`unref` 或代码库已有统一适配函数；禁止通过裸 `any`、多层可选链或同时兼容多种未知结构的表达式掩盖契约不明确。
- 表单提交必须形成可追溯的校验闭环：Req DTO 或已确认契约中的必填性映射到 `el-form-item prop` 和 `rules`，提交处理先调用 `formRef.validate()`，校验通过后才调用 API。目标代码库使用等价表单组件或校验库时，可沿用其既有机制，但必须具备同等阻断效果。
- 主题和 i18n 细则只按 `i18n-theme.md` 执行。
- 文件式路由语法只按 `file-based-routing.md` 执行。
- 文件式路由生成路由页面时，必须生成 `definePage({ name })`；涉及 layout 菜单时必须生成 `definePage({ name, meta: { menu } })`，并显式判断 `hidden`：列表、首页、仪表盘、独立配置页且可从菜单直接访问时为 `false`；动态参数页、`add/create/edit/update/detail/view` 语义页、按钮或行操作进入的业务流程操作页为 `true`；用户或设计明确要求作为菜单展示时可为 `false`，但路径不得依赖动态参数。文件式路由菜单页面必须读取 `menuPageContext.common.finalMenuPath` 和 `menuPageContext.frontend`；页面文件按 `frontend.menuFilePath` 落位，路由必须等于 `frontend.routePath` 和 `common.finalMenuPath`。非菜单页面不受菜单入口 `index.vue` 规则约束。
- 普通业务菜单不得在 `meta.menu` 中手写 `path`；layout 菜单 path 必须由 `router.getRoutes()` 的最终 `route.path` 补齐。`hidden: true` 页面必须设置 `parentNodeId`。
- 组件 props/events/slots/methods 只按 `magus-framework-ui.md` 指向的组件事实源执行。
- 目标项目真实代码与本技能默认基线冲突时，以目标项目真实代码为准，并在交付说明中记录取舍；但不得覆盖全局硬门禁或共享 `menuPageContext` 中已确认的菜单页面映射。

## 交付要求

交付说明必须包含：

- 读取来源：需求/接口/项目规范、本技能和用到的 references。
- 确认变量：API、权限、字典、路由、主题、i18n 和组件选择。
- 修改内容：API、页面、组件、语言包、样式、权限、字典、路由。
- 验证结果：命令、退出码或浏览器检查结果；无法验证时说明原因和剩余风险。

不得声称完成未验证的功能；不得把模板、示例数据、示例接口、示例权限码或未接入语言包当作可交付代码。

## 总自检清单

### 类型与契约

- [ ] 类型落位、命名、职责拆分、mapper、必填性和 `import type` 已按 `type-definition-standard.md` 检查，且前端类型与后端 DTO / `apiContractContext` 无 P0/P1 不一致。

### API

- [ ] API 服务前缀、最终 URL、请求方法、参数位置、分页字段、响应解包和权限/字典使用已按 `api-permission-dictionary.md` 检查，且不存在自行推演的路径或字段。

### 路由菜单

- [ ] 文件式路由、`definePage`、layout 菜单、`menuPageContext` 和页面跳转闭环已按 `file-based-routing.md` 检查。

### 组件与状态

- [ ] 页面分层、组件边界、composable 职责、新增/编辑/详情路由与 `XxxForm` 抽取条件、表单校验闭环、loading/empty/error/selection 状态已按 `module-development-standard.md` 和组件 reference 检查。

### 验证与运行时

- [ ] 已执行项目可用的类型检查、构建、SFC parse 或等价验证；wujie/shadow DOM、ECharts、首屏空白页风险已按相关 reference 检查或记录环境阻断。
