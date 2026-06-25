# MgDialog

对话框组件，基于 Element Plus `ElDialog` 封装。

用于：表单弹窗、确认提示、详情展示。

---

## Usage

```vue
<MgDialog v-model="visible" title="编辑用户" width="600px" @open="handleOpen">
  <el-form :model="form" label-width="100px">
    <el-form-item label="姓名">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-form-item label="邮箱">
      <el-input v-model="form.email" />
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="visible = false">取消</el-button>
    <el-button type="primary" @click="handleSubmit">确定</el-button>
  </template>
</MgDialog>
```

```ts
import { reactive, ref } from 'vue'

const visible = ref(false)
const form = reactive({ name: '', email: '' })

const handleOpen = () => {
  console.log('对话框已打开')
}

const handleSubmit = () => {
  console.log('提交表单:', form)
  visible.value = false
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| modelValue | `boolean` | 否 | `false` | 对话框是否显示 |
| title | `string` | 否 | `''` | 对话框标题 |
| width | `string \| number` | 否 | `'50%'` | 对话框宽度 |
| fullscreen | `boolean` | 否 | `false` | 是否全屏显示 |
| modal | `boolean` | 否 | `true` | 是否显示遮罩层 |
| closeOnClickModal | `boolean` | 否 | `true` | 点击遮罩层是否关闭 |
| closeOnPressEscape | `boolean` | 否 | `true` | 按 ESC 是否关闭 |
| showClose | `boolean` | 否 | `true` | 是否显示关闭按钮 |
| draggable | `boolean` | 否 | `false` | 是否可拖动 |
| center | `boolean` | 否 | `false` | 标题和底部是否居中 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| update:modelValue | `boolean` | 对话框显示/隐藏状态改变时触发 |
| open | `void` | 对话框打开时触发 |
| close | `void` | 对话框关闭时触发 |
| opened | `void` | 对话框打开动画完成时触发 |
| closed | `void` | 对话框关闭动画完成时触发 |

---

## Slots

| 插槽名 | Props | 说明 |
|---|---|---|
| default | `void` | 对话框主体内容 |
| header | `void` | 对话框头部内容（会替换默认标题栏） |
| footer | `void` | 对话框底部内容（会替换默认底部按钮区） |

---

## AI Usage Rules

1. 使用 `v-model` 控制显示/隐藏。
2. `modal` 为 `true` 时显示遮罩层，`closeOnClickModal` 控制点击遮罩是否关闭。
3. `header` 插槽会替换默认标题栏，`footer` 插槽会替换默认底部区域。
4. `fullscreen` 为 `true` 时对话框会撑满屏幕。
