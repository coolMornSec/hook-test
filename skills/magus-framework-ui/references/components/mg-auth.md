# MgAuth

权限控制组件，根据授权码列表判断是否展示组件内容。

用于：按钮权限控制、菜单权限控制、功能区域显示隐藏。

---

## Usage

```vue
<MgAuth :codes="codes" modifer="or">
  <MgButton type="primary">查看个人信息</MgButton>
</MgAuth>
```

```ts
const codes = ['superAdmin', 'admin']
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| codes | `string[]` | 是 | `[]` | 授权码列表 |
| modifer | `'or' \| 'and'` | 否 | `'or'` | 校验修饰符：`or` 表示任一匹配即显示，`and` 表示全部匹配才显示 |

---

## AI Usage Rules

1. `codes` 为必填项，不传时默认不显示内容。
2. `modifer` 为 `'or'` 时，用户拥有任一授权码即显示内容。
3. `modifer` 为 `'and'` 时，用户必须拥有全部授权码才显示内容。
4. 组件通过内置逻辑获取当前用户权限码，无需手动传入用户权限。
