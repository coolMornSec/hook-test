# Framework UI Bridge

此文件只作为 `magus-frontend-vue-guide` 到 `magus-framework-ui` 组件事实源的导航桥，不重复维护组件 API。

## 读取顺序

开发模块并使用 Magus UI 组件时，按以下顺序读取事实源：

1. `../../magus-framework-ui/SKILL.md`：组件选择优先级、真实项目基线、标准列表布局、权限/字典/反馈规则。
2. `../../magus-framework-ui/references/ui-manifest.md`：组件、composable、类型索引。
3. `../../magus-framework-ui/references/best-practices.md`：表格满高、分页、弹窗、表单和可访问性实践。
4. `../../magus-framework-ui/references/components/[component].md`：具体组件 props/events/slots/methods。
5. `../../magus-framework-ui/references/composables/*.md`：只有使用对应 composable 时读取。
6. `../../magus-framework-ui/references/types/*.md`：只有使用对应类型时读取。

## 组件优先级

模块开发中的默认组件优先级：

`@magustek/framework-ui` > `@magustek/framework-biz-ui` > Element Plus > 自定义组件。

组件选择场景见 `component-tool-selection.md`；本文件不重复维护场景表。

## 冲突处理

- 如果本技能与 `magus-framework-ui` 的具体组件 API 冲突，以 `magus-framework-ui` 对应 component reference 为准。
- 如果目标项目已有同类组件封装，以目标项目真实代码为准。
- 冲突和回退原因必须写入交付说明。

## 边界

- 不在本文件复制组件 props/events/slots/methods。
- 不在本文件定义页面流程、API、权限、字典、主题或 i18n。
