# MgIcon

图标渲染组件，支持 Element Plus 字体图标和 SVG 图标。

用于：内联图标展示、带尺寸和颜色的图标渲染。

---

## Usage

```vue
<!-- 字体图标 -->
<MgIcon name="wenjianjia" size="20" color="#409eff" />

<!-- SVG 图标（使用 icon 属性，优先级高于 name） -->
<MgIcon icon="search" size="20" color="#30429b" />

<!-- SVG 图标（使用 name 属性） -->
<MgIcon name="svg-search" size="20" color="#30429b" />
```

```ts
import { MgIcon } from '@magustek/framework-ui'
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| name | `string` | 否 | `''` | 图标名称，可传字体图标名或 SVG 图标名 |
| icon | `string \| object` | 否 | `''` | 图标标识，与 `name` 二选一，优先级比 `name` 高 |
| size | `number \| string` | 否 | `'1em'` | 图标大小 |
| color | `string` | 否 | `'currentColor'` | 图标颜色 |

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| default | `void` | 自定义内容 |

---

## AI Usage Rules

1. `icon` 和 `name` 二选一，`icon` 优先级更高。
2. SVG 图标可通过 `icon` 或 `name` 两种方式传入。
3. 字体图标仅使用 `name` 传入。
