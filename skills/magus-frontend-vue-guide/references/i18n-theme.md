# i18n and Theme

国际化和主题策略规范说明

## i18n 开关

`useI18n` 是硬开关，必须来自用户、需求文档或目标项目规范。

- `useI18n = false`：允许使用清晰中文业务文案；不要创建未合并的语言文件或无引用 key。
- `useI18n = true`：所有页面标题、按钮、表单 label、placeholder、表格列、空态、确认弹窗、成功/失败消息、校验提示都必须接入 i18n。
- 若目标项目已经强制 i18n，即使用户说不需要，也应指出冲突并按项目规范或回到确认阶段处理。

## 既有 i18n 项目增加模块

1. 读取 `src/lang`、`createI18n`、`mergeLocalMessages`、`useLocale`、Element Plus locale、`useMgUiMsg()` 和 `useBizUiMsg()` 合并方式。
2. 识别语言集合，例如 `cn`、`en`，不要自行新增语言。
3. 建立模块命名空间，例如 `system.role`。命名空间必须是页面 key 和语言文件对象共同使用的完整路径，不能只在页面代码中使用外层命名空间。
4. 使用 `mergeLocalMessages` 注册模块语言包时，第一层 key 必须是 locale 编码，例如 `cn`、`en`，第二层开始才是业务命名空间；不得把业务命名空间直接作为第一层传入。
5. 为页面、字段、按钮、消息、校验、空态生成 key。
6. 确保语言文件被真实合并到 i18n 实例，不创建孤立文件。
7. 验证语言切换后不出现 key 原文、空白或混合硬编码。

示例 key 结构：

```ts
export default {
  system: {
    role: {
      title: '角色管理',
      field: {
        name: '角色名称',
        code: '角色编码',
      },
      action: {
        create: '新增角色',
      },
      message: {
        saveSuccess: '保存成功',
      },
    },
  },
}
```

如果页面使用 `t('xx.info.title')` 或 `$t('xx.info.title')`，语言文件必须保留完整外层：

```ts
export default {
  xx: {
    info: {
      title: '空间管理',
    },
  },
}
```

注册到 i18n 实例时，也必须保留 locale 包裹层：

```ts
i18n.mergeLocalMessages({
  cn: {
    xx: {
      info: {
        title: '空间管理',
      },
    },
  },
  en: {
    xx: {
      info: {
        title: 'Space Management',
      },
    },
  },
})
```

禁止生成下面这种缺少外层命名空间的结构，因为页面会查找不到 `xx.info.title`：

```ts
export default {
  info: {
    title: '空间管理',
  },
}
```

也禁止把业务命名空间误作为 `mergeLocalMessages` 的第一层 key：

```ts
i18n.mergeLocalMessages({
  xx: {
    info: {
      title: '空间管理',
    },
  },
})
```

## 非 i18n 项目增量引入 i18n

这是跨模块改造，不是普通页面开发。只有计划明确授权时才做：

- 增加或调整 `src/lang/index.ts`，接入 `createI18n`、`mergeLocalMessages`、`withGlobalLocale`。
- 保留 Magus UI/Biz UI 消息合并，避免组件库文案失效。
- 在 `App.vue` 通过 `ElConfigProvider` 和 `useLocale()` 派生 Element Plus 语言。
- 替换本模块用户可见文案，并说明是否需要后续全站迁移。

## 主题开关

`requiresCustomTheme` 是硬开关，必须来自用户、设计文档或计划。

- `false`：沿用项目现有 Element Plus token、Magus 变量、SCSS/Tailwind/UnoCSS 风格。新增样式只解决布局、尺寸、状态。
- `true`：只使用确认过的 `themeSource` 或 `themeTokens`；缺 token 时继续确认。

## 主题颜色修改

默认优先级：

1. 复用已有 CSS 变量或 Element Plus token。
2. 模块 scoped 样式中声明局部变量。
3. 只有明确要求全局主题时，才修改 `src/styles/theme.scss` 或全局样式入口。

至少覆盖并检查：

- 主色、背景、边框、正文、弱文本。
- 成功、警告、危险、信息状态色。
- hover、active、disabled。
- 按钮、表格、表单、弹窗、分页、固定操作列。

禁止根据“科技感”“高级”“清爽”等形容词自行生成色板。

## 验证

- i18n：切换每种已支持语言，检查页面、表单、表格、弹窗、消息和校验。
- 主题：桌面视口检查对比度、状态色、表格高度、分页和按钮栏稳定性。
- 全局主题变更：必须回归至少一个既有模块，确认未破坏默认 Magus 风格。

## 避免问题

1. 国际化没有添加命名空间显示失败
