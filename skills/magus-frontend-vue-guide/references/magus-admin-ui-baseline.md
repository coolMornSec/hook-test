# Magus Admin UI Baseline

本文件是Magus 默认微前端后台的基线事实。目标项目没有同类代码可参考时，使用本文件辅助判断默认技术栈、目录、页面风格和业务页基线。具体开发规则仍以专题 reference 为准。

## 技术栈基线

- Vue 3 + TypeScript + Composition API + `<script setup lang="ts">`。
- Vite 5，`base`、开发端口、代理目标、构建输出目录来自 `VITE_APP_BASE`、`VITE_APP_PORT`、`VITE_APP_SERVER_URL`。
- `VITE_APP_BASE` 只保存微应用部署路由值本身，不含首尾 `/`；微前端部署下必须非空。
- 只有用户明确声明非微前端站点根部署时才允许 `VITE_APP_BASE` 为空，并必须记录例外来源；默认不得推荐空值。
- Element Plus 2.x、Pinia、Vue Router、Vue I18n、VueUse、Tailwind CSS + SCSS。
- Magus 依赖优先使用 `@magustek/framework-core`、`@magustek/framework-ui`、`@magustek/framework-biz-ui`、`@magustek/framework-biz-utils`、`@magustek/framework-wujie`、`@magustek/icon-svg`。
- 自动导入和组件解析由 `unplugin-auto-import`、`unplugin-vue-components` 配置；未确认自动导入时显式 import。

## 目录基线

默认 Magus 文件常见于：

- API 常见于 `src/api/[module]/index.ts`，手写契约类型位于 `src/api/[module]/types.ts`
- 手写路由常见于 `src/router/index.ts`
- 微前端主路由常见于 `src/mainRouter/`
- 页面常见于 `src/pages/[module]/`
- 模块语言包常见于 `src/lang/[module]/lang/{cn,en}.ts`
- 全局语言入口常见于 `src/lang/index.ts`
- 样式入口常见于 `src/styles/`

实际目录规则见 `module-development-standard.md`。

文件式路由项目可以使用 `src/pages` 结构；具体路由规则见 `file-based-routing.md`。

## 页面风格基线

- 整体是企业后台工作台，不做 landing page、hero、营销介绍、装饰插画或渐变背景。
- 主背景使用 `#f3f6fb` / `#f5f7fa`，内容区使用白色或 `var(--el-bg-color)`。
- 主色使用 `#30429b` 或 `var(--el-color-primary)`；边框使用 `#dcdfe6`、`#e4e7ed`。
- 正文使用 `#333`，次级文本使用 `#606266` / `#909399`。
- 字体使用 `Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif`。
- 页面布局优先撑满容器：`flex h-full min-h-0 flex-col overflow-hidden`。

## 业务页基线入口

目标项目没有同类模块可参考时，默认业务页形态如下：

- 列表页使用 `MgLayout`、`MgSearch`、`MgToolbar`、`MgTable`。
- 新增、编辑、详情默认使用独立路由页和 `MgBackWrap`；存在复用或表单字段超过 3 个时，默认抽 `components/XxxForm.vue`。
- 行操作、分页、选择、确认、返回和表单状态规则见 `module-development-standard.md`。
- API、权限、字典规则见 `api-permission-dictionary.md`。

本文件只提供默认基线信号，不重复维护列表页和表单页开发细则。

## 公共样式基线

```scss
.full-height-tabs {
  @apply box-border flex h-full flex-col;
}

.full-height-tabs .el-tabs__content {
  @apply flex-1;
}

.full-height-tabs .el-tabs__content .el-tab-pane {
  @apply flex h-full flex-col overflow-auto;
}

.el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content {
  @apply rounded bg-[#E8EAED] #{!important};
}

.mg-table-flex {
  @apply flex flex-1 flex-col overflow-auto;
}

.search-filter {
  @apply mr-[10px];

  &-label {
    @apply mr-[10px] inline-block;
  }

  &-content {
    @apply inline-block min-w-[180px];
  }
}
```

## 生成禁止项

- 不生成测试 token、无意义生命周期日志、演示 mock 数据、装饰性背景。
- 不在文档外新增字段、按钮、流程、接口、权限码或字典 code。
- 不用模板示例接口地址、权限码、路由名替代已确认契约。

## 边界

- 本文件提供默认基线，不覆盖目标项目现有代码。
- 页面分层和状态交互见 `module-development-standard.md`。
- API 细节见 `api-permission-dictionary.md`。
- 组件选型见 `component-tool-selection.md`。
- 主题/i18n 变更见 `i18n-theme.md`。
