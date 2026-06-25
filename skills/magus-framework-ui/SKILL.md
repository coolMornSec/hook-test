---
name: magus-framework-ui
description: Use when selecting, combining, or falling back from Magus enterprise UI components. This skill defines component priority, usage guidance, and common UI composition templates for `@magustek/framework-ui`, `@magustek/framework-biz-ui`, and Element Plus.
---

# Magus Framework UI

本技能只负责 **组件选择优先级、组件使用规范、常见业务页面拼装模板**。

## 输入与输出边界

- 适用条件：已有 Magus 前端项目中的组件选型、页面组合和 Element Plus 回退判断。
- 必要输入：页面场景、交互要求、数据规模、视觉方向和真实组件事实源。
- 标准输出：组件选型表、页面组合方式、props/events/slots 依据、回退理由和实现约束。
- 不负责：项目骨架、完整业务逻辑、虚构组件能力、独立决定接口或权限契约。

如需要项目骨架、业务开发或架构配置时，交给对应技能处理。

## 技能定位

`magus-framework-ui` 是一个 **组件使用规范技能**，用于指导 AI 在已有 Magus 前端项目中完成页面拼装与组件选型。

它的目标不是“写完整业务”，而是帮助 AI 稳定回答以下问题：

- 这个场景优先用哪个组件。
- 这个页面应该如何组合组件。
- 哪些场景适合回退到 Element Plus。
- 哪些内容必须使用 Biz UI 组件而不是普通表单控件。
- 哪些模板适合复用，如何把模板映射到真实业务页面。
- 如何避免过度设计和虚构组件能力。

## 核心原则

1. 先确认现有组件的真实能力边界，再决定使用方式。
2. 优先复用 Magus 组件；只有覆盖不足时才回退。
3. 优先输出可组合的页面范式，而不是散乱的组件清单。
4. 只写已确认事实，不编造组件 API、props、事件、slot 或行为。

## 组件选择优先级

1. `@magustek/framework-ui`
   - 通用布局、表格、搜索、弹窗、分页、树、分栏、图标、日期、流程图、裁剪等基础能力。
2. `@magustek/framework-biz-ui`
   - 用户、组织、职务、工作组、资源、字典、上传、返回包装、权限判断等业务能力。
3. Element Plus
   - 当 Magus 组件未覆盖，或原生能力更合适时使用。
4. 自定义组件
   - 只有在前两层都不能表达，且复用价值明确时才创建。

回退到 Element Plus 或自定义组件时，需要说明原因：

- Magus 组件是否不存在。
- 现有项目是否已经明确采用 Element 原生写法。
- 是否存在特殊交互、布局或性能约束。

## 使用前门禁

在使用某个 Magus 组件前，必须先读取该组件对应的说明、references、assets 或模板，确认它的真实能力后再使用。

如果要写一个页面模板，必须先确认：

- 页面类型：列表 / 新增编辑 / 详情 / 树表 / 弹窗流程。
- 组件边界：哪些内容交给 `framework-ui`，哪些交给 `framework-biz-ui`。
- 是否已有项目既定写法可复用。

## 读取与依赖原则

- 目标项目已有依赖时，不重复安装。
- 如果依赖缺失或项目为新建骨架，先确认包管理器与私服配置，再决定安装。
- 若项目配置了自动导入和组件解析，页面不手动 import 已自动导入的组件。
- 未配置自动导入时，按项目现有模式按需 import。

## 文件导航

在引用组件能力、模板或示例时，必须显式说明来源文件，并按下面顺序导航：

1. `SKILL.md`：读取本技能的总规则、组件优先级、模板说明。
2. `ui-manifest.md`: 读取组件列表和对应导航地址。
3. `references/components/*.md`：读取具体组件说明、使用约束、最佳实践；如果目标目录存在该类文件，优先引用。
4. `assets/*.vue`：读取可复用的页面模板或组合示例。
5. 目标项目真实页面或模块文件：将模板映射到实际业务场景。
6. `references/types`: 组件相关的type类型。

引用时必须写清楚“用途 + 来源文件 + 适用场景”。

### 组件引用映射

当需要确认组件能力时，优先按下面的映射读取对应文件；如果目标目录不存在对应 `references` 文件，则回退到本技能和 `assets` 模板，不得假装已读取不存在的文件。

| 组件 | 优先来源文件 | 说明 |
|---|---|---|
| `MgLayout` | `references/components/mg-layout.md` | 页面布局与内容区组织方式 |
| `MgSearch` | `references/components/mg-search.md` | 搜索区结构、折叠区与触发方式 |
| `MgToolbar` | `references/components/mg-toolbar.md` | 列表工具栏与操作按钮组织 |
| `MgTable` | `references/components/mg-table.md` | 表格、分页、selection、固定列 |
| `MgPageTable` | `references/components/mg-page-table.md` | 搜索 + 工具栏 + 表格组合 |
| `MgDialog` | `references/components/mg-dialog.md` | 弹窗结构、footer、确认流程 |
| `MgTree` | `references/components/mg-tree.md` | 树形展示、懒加载、选中态 |
| `MgTabs` / `MgTabPane` | `references/components/mg-tabs.md` | 标签页分组与切换 |
| `MgTabButton` | `references/components/mg-tab-button.md` | 紧凑切换按钮 |
| `MgPaging` | `references/components/mg-paging.md` | 分页器使用方式 |
| `MgButton` | `references/components/mg-button.md` | 按钮封装与项目约定 |
| `MgDatePicker` / `MgTimePicker` | `references/components/mg-date-time-picker.md` | 日期时间选择 |
| `MgCascader` | `references/components/mg-cascader.md` | 级联选择 |
| `MgIcon` / `MgIconPicker` / `useMgIcon` | `references/components/mg-icon.md` | 图标展示与选择 |
| `MgCropper` / `useCropper` | `references/components/mg-cropper.md` | 图片裁剪 |
| `MgAddTemplate` | `references/components/mg-add-template.md` | 添加模板入口 |
| `MgEsign` | `references/components/mg-esign.md` | 手写签名 |
| `MgComplexSelect` | `references/components/mg-complex-select.md` | 组织、用户、职务等复杂选择 |
| `MgResourceSelect` | `references/components/mg-resource-select.md` | 菜单、按钮、资源选择 |
| `MgUpload` | `references/components/mg-upload.md` | 文件上传 |
| `MgDict` | `references/components/mg-dict.md` | 字典展示与选择 |
| `MgBackWrap` | `references/components/mg-back-wrap.md` | 返回头表单/详情外壳 |
| `MgAuth` | `references/components/mg-auth.md` | 权限显示控制 |

引用模板时必须写清楚“用途 + 来源文件 + 适用场景”，例如：

- 标准列表页模板，来源 `assets/user-management.vue`，适用于用户管理、角色管理等典型 CRUD 页面。
- 组件说明来源 `references/components/mg-table.md`，用于确认表格分页、固定列和空态能力。

## 组件清单与使用说明

### `@magustek/framework-ui`

| 组件/函数 | 用途 | 优先场景 | 备注 |
|---|---|---|---|
| `MgLayout` | 页面布局容器 | 列表页、工作台页、搜索+内容区布局 | 作为列表页基础骨架优先使用 |
| `MgSearch` | 搜索区容器 | 多条件筛选、展开更多 | 搜索条件集中展示时优先使用 |
| `MgToolbar` | 列表工具栏 | 新增、批量删除、导入导出等操作 | 与列表页主内容区域配合使用 |
| `MgTable` | 表格+分页封装 | 标准列表页默认选择 | 用于承载表格与分页的主区域 |
| `MgPageTable` | 搜索+工具栏+表格组合 | 简单 CRUD 页面快速拼装 | 适合标准列表页快速落地 |
| `MgDialog` | 统一弹窗 | 局部流程、辅助选择、预览、确认操作 | 不承载主业务大表单 |
| `MgTree` | 树形展示 | 左树右表、组织/资源树 | 适合分类、目录、组织结构 |
| `MgTabs` / `MgTabPane` | 标签页 | 详情分组、业务分组 | 适合同页分块内容切换 |
| `MgTabButton` | 按钮式标签 | 状态切换、分类切换 | 适合紧凑型分类筛选 |
| `MgPaging` | 分页 | 自定义表格时补充分页能力 | 当页面不是 `MgTable` 时使用 |
| `MgButton` | 按钮封装 | 项目已有使用时优先 | 以项目已有写法为准 |
| `MgDatePicker` / `MgTimePicker` | 日期时间选择 | 替换对应 Element 组件 | 仅在项目已有该写法时优先使用 |
| `MgCascader` | 级联选择 | 替换 Element Cascader | 用于层级数据选择 |
| `MgIcon` / `MgIconPicker` / `useMgIcon` | 图标展示与选择 | 菜单图标、配置页 | 图标选择与展示场景优先 |
| `MgCropper` / `useCropper` | 图片裁剪 | 头像、Logo 上传前处理 | 适合图片预处理流程 |
| `MgAddTemplate` | 添加模板 | 项目已有模板化新增场景 | 仅在已有模板模式下使用 |
| `MgEsign` | 签名 | 手写签名场景 | 仅用于签名业务 |

### `@magustek/framework-biz-ui`

| 组件 | 用途 | 优先场景 | 备注 |
|---|---|---|---|
| `MgComplexSelect` | 用户、组织、职务、工作组、关系组合选择 | 平台级复杂选择器 | 优先用于平台基础对象选择 |
| `MgResourceSelect` | 应用、菜单、按钮、资源选择 | 权限、资源配置 | 适合权限与资源树选择 |
| `MgUpload` | 文档/文件上传 | 业务文件上传 | 用于业务附件、资料上传 |
| `MgDict` | 字典显示或字典选择入口 | 字典展示、字典选择 | 优先复用字典能力 |
| `MgBackWrap` | 带返回头的表单/详情外壳 | 新增、编辑、详情页 | 表单页首选外壳 |
| `MgAuth` | 权限判断展示组件 | 按钮、区域、字段显示控制 | 用于按权限显示内容 |

## 组件使用规则

### 1. 列表页优先模板

标准列表页优先使用：`MgLayout` + `MgSearch` + `MgToolbar` + `MgTable`。

原则：

- 搜索区放在 header。
- 工具栏放在 main 顶部。
- 表格占据剩余空间。
- 列表页不优先用大卡片包裹整个页面。
- 行操作按钮使用 link / small 风格，右侧固定。
- 批量按钮要跟随选择状态禁用或启用。

### 2. 表单页优先模板

- 主新增/编辑页优先使用 `MgBackWrap`。
- 表单主体保持白底、紧凑、可扫描。
- 常见字段宽度按页面内容决定，避免整页拉满。
- 复杂表单优先拆为表单组件，再由页面负责加载和提交。
- `MgDialog` 只用于局部流程，不承载主业务大表单。

### 3. 树、分栏与授权

- 左树右表优先 `MgLayout` + `MgTree` + `MgTable`。
- 资源、菜单、权限相关选择优先 `MgResourceSelect`、`MgComplexSelect` 或已有 Biz UI 组件。
- 不手写复杂树穿梭、复杂选择器，除非设计已经明确要求且现有组件无法满足。
- 页面根容器优先直接使用 `MgLayout` 或 `MgBackWrap`，不要为了样式额外增加空白包裹层。
- 只有当容器承担明确布局职责时，才新增中间层；禁止为了“看起来整齐”而堆叠无意义 `div`。

### 4. 反馈与状态

- loading 绑定到按钮、表格或局部容器。
- 删除、批量操作、敏感动作必须有确认。
- 字典展示优先组件化，不在每行重复请求。
- 权限展示优先 `v-auth` 或 `MgAuth`，按项目既有方式使用。

## 常见模板

模板模块用于给 AI 提供**可直接复用的页面拼装参考**，不是业务成品代码。

### 模板使用场景

- 需要快速搭建标准后台列表页时。
- 需要构建左树右表、详情分组或表单页时。
- 需要展示 `MgLayout`、`MgSearch`、`MgToolbar`、`MgTable`、`MgBackWrap` 等组件的组合关系时。
- 需要 AI 先按模板理解页面结构，再映射到目标项目真实字段与接口时。

### 模板读取原则

- 模板只用于理解页面结构和组件组合方式。
- 模板代码必须结合目标项目真实字段、真实接口、真实权限和真实目录使用。
- 不把模板中的示例字段、示例按钮、示例状态直接写入生产代码。
- 如需更具体的页面形态，优先引用 `assets` 中的对应模板文件。

### 参考模板

- 标准列表页模板：`/assets/user-management.vue`
  - 适用于用户管理、角色管理、字典管理等典型后台 CRUD 页面。
  - 展示搜索区、工具栏、表格、行操作、弹窗表单的典型拼装方式。
  - 关联组件：
  - 适合需要快速理解“列表 + 筛选 + 新增编辑 + 删除”闭环的场景。

- 左右布局模板：`/assets/user-management.vue`
  - 适用于组织管理、资源管理、菜单管理、分类管理、字典管理等典型树表结合页面。
  - 展示树、搜索区、工具栏、表格、行操作、弹窗表单的典型拼装方式。
  - 关联组件：MgLayout、MgTree、MgTable
  - 适合需要快速理解“树结构驱动表格内容”的场景。

- 基础业务表单模板：`/assets/user-management.vue`
  - 适用于新增表单页、编辑表单页、详情展示页、需要返回头和紧凑表单布局的业务页面。
  - 展示树、搜索区、工具栏、表格、行操作、弹窗表单的典型拼装方式。
  - 关联组件：`MgBackWrap`、`MgUpload`、`MgCropper`
  - 适合需要快速理解“树结构驱动表格内容”的场景。

## 事实约束

- 不要在 `MgTable`、`MgToolbar`、`MgSearch` 意外添加无用重复的容器。
- 不要把 Element Plus 当作默认首选。
- 不要把业务选择器改写成普通下拉框，除非数据量和交互明确适合。
- 不要杜撰不存在的组件名、prop、slot、事件或默认行为。
- 不要把本技能写成项目初始化或开发总技能。

## 交付自检

在生成任何组件方案前，检查以下问题：

- 是否已优先使用 `@magustek/framework-ui` 或 `@magustek/framework-biz-ui`。
- 是否明确说明了回退到 Element Plus 的原因。
- 是否按列表、表单、树表等常见模板组合。
- 是否避免了冗余卡片、装饰性视觉和过度设计。
- 是否完整阅读使用组件的能力。
