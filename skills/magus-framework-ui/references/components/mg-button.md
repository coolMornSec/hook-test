# MgButton

按钮组件，基于 Element Plus `ElButton` 封装。

用于：页面操作按钮、表单提交按钮、工具栏按钮。

---

## Usage

```vue
<MgButton type="primary">主要按钮</MgButton>
<MgButton type="success">成功按钮</MgButton>
<MgButton type="warning">警告按钮</MgButton>
<MgButton type="danger">危险按钮</MgButton>
<MgButton type="plain" loading>加载中</MgButton>
```

```ts
import { MgButton } from '@magustek/framework-ui'
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| type | `string` | 否 | `'default'` | 按钮类型：`default` / `primary` / `success` / `warning` / `danger` |
| size | `string` | 否 | `'default'` | 按钮大小：`default` / `large` / `small` |
| disabled | `boolean` | 否 | `false` | 是否禁用 |
| loading | `boolean` | 否 | `false` | 是否加载中 |
| icon | `string` | 否 | `''` | 图标 |
| round | `boolean` | 否 | `false` | 是否圆角 |
| circle | `boolean` | 否 | `false` | 是否圆形按钮 |
| plain | `boolean` | 否 | `false` | 是否朴素按钮 |
| text | `boolean` | 否 | `false` | 是否文本按钮 |
| link | `boolean` | 否 | `false` | 是否链接按钮 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| click | `void` | 点击按钮时触发 |

---

## AI Usage Rules

1. `type` 控制按钮风格，不传时使用默认按钮。
2. `loading` 为 `true` 时按钮显示加载图标且不可点击。
3. `circle` 为 `true` 时按钮为圆形，适合纯图标按钮。
4. `plain` 为 `true` 时按钮为朴素风格（边框+文字色，背景透明）。
5. `text` 和 `link` 为文本和链接风格按钮，无边框无背景。
