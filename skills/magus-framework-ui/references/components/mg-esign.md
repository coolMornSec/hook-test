# MgEsign

电子签名组件，用于手写签名和获取签名数据。

用于：合同签署、审批签名、手写批注。

---

## Usage

```vue
<MgEsign ref="esignRef" />
<el-button @click="handleSave">保存签名</el-button>
<el-button @click="handleClear">清空</el-button>
```

```ts
import { ref } from 'vue'
import type { MgEsignInstance } from '@magustek/framework-ui'

const esignRef = ref<MgEsignInstance>()

const handleSave = () => {
  const signature = esignRef.value?.getSignature()
  console.log('签名数据:', signature)
}

const handleClear = () => {
  esignRef.value?.clear()
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| width | `number \| string` | 否 | `'100%'` | 签名板宽度 |
| height | `number \| string` | 否 | `'300px'` | 签名板高度 |
| lineWidth | `number` | 否 | `2` | 笔画宽度 |
| lineColor | `string` | 否 | `'#000'` | 笔画颜色 |

---

## Methods

通过组件 `ref` 调用。

| 方法名 | 参数 | 返回值 | 说明 |
|---|---|---|---|
| getSignature | `void` | `string` | 获取签名数据（base64 图片） |
| clear | `void` | `void` | 清空签名 |
| undo | `void` | `void` | 撤销上一步 |

---

## Types

```ts
export interface MgEsignInstance {
  getSignature: () => string
  clear: () => void
  undo: () => void
}
```

---

## AI Usage Rules

1. 所有方法必须通过组件 `ref` 调用。
2. `getSignature` 返回 base64 图片数据。
