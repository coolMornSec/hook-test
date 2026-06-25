# MgBackWrap

返回包装组件，用于显示返回按钮和标题，包裹详情页内容。

用于：详情页顶部返回、子页面导航。

---

## Usage

```vue
<MgBackWrap title="编辑用户" @back="handleBack">
  <el-form :model="form" label-width="80px" style="max-width: 600px">
    <el-form-item label="用户名">
      <el-input v-model="form.username" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submit">保存</el-button>
      <el-button @click="handleBack">取消</el-button>
    </el-form-item>
  </el-form>
</MgBackWrap>
```

```ts
const form = reactive({
  username: '',
})
const handleBack = () => {
  // 返回上一页
}
const submit = () => {
  // 保存
  console.log(form)
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| title | `string` | 否 | `''` | 标题文本 |
| showBack | `boolean` | 否 | `true` | 是否显示返回按钮 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| back | `void` | 点击返回按钮时触发 |

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| default | `void` | 内容区域 |
| title | `void` | 标题区域（会替换默认的文本标题） |

---

## AI Usage Rules

1. `showBack` 为 `true` 时显示返回按钮，点击触发 `back` 事件。
2. `title` 插槽可完全自定义标题展示。
3. 默认插槽内的内容会在标题下方渲染。
