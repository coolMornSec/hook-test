# MgScrollbar

滚动条组件，基于 Element Plus `ElScrollbar` 封装，用于自定义滚动条样式。

用于：内容区域美化滚动条、固定高度区域的滚动容器。

---

## Usage

```vue
<MgScrollbar style="height: 400px">
  <p v-for="i in 100" :key="i">第 {{ i }} 行内容</p>
</MgScrollbar>
```

```ts
import { MgScrollbar } from '@magustek/framework-ui'
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| height | `number \| string` | 否 | `-` | 滚动条高度 |
| maxHeight | `number \| string` | 否 | `-` | 最大高度 |
| native | `boolean` | 否 | `false` | 是否使用原生滚动条 |
| wrapStyle | `Record<string, string \| number>` | 否 | `{}` | 包装元素样式 |
| wrapClass | `string` | 否 | `''` | 包装元素类名 |
| viewClass | `string` | 否 | `''` | 视图元素类名 |

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| default | `void` | 滚动内容 |

---

## AI Usage Rules

1. 需明确设置容器高度（通过 `style` 或 `height` prop），否则滚动条不生效。
2. `native` 为 `true` 时使用浏览器原生滚动条，忽略美化样式。
