# MgUpload

文件上传组件，基于 Element Plus `ElUpload` 封装。

## Usage

```vue
<MgUpload v-model="fileIds" />
```

```ts
import { ref } from 'vue'

const fileIds = ref<string[]>(['文件 id'])
```

## Props

支持 Element Plus `ElUpload` 原生属性。

扩展属性：

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| modelValue | `string[]` | 否 | `[]` | 文件 ID 数组（支持 `v-model`） |
| useDefault | `boolean` | 否 | `true` | 是否使用默认上传逻辑 |

## AI Usage Rules

1. 通过 `v-model` 绑定文件 ID 数组。
2. `useDefault` 为 `true` 时使用组件内置的上传逻辑，为 `false` 时需自行处理上传。
3. 可透传 Element Plus `ElUpload` 原生属性。

---
