# MgCropper

图片裁剪组件，用于裁剪和编辑图片。

用于：头像裁剪、封面图裁剪、图片尺寸调整。

---

## Usage

```vue
<MgCropper :src="imageSrc" :config="cropperConfig" @crop="handleCrop" />
```

```ts
import { ref } from 'vue'

const imageSrc = ref('/path/to/image.jpg')
const cropperConfig = {
  aspectRatio: 16 / 9,
  autoCropArea: 0.8
}

const handleCrop = (data: object) => {
  console.log('裁剪数据:', data)
}
```

---

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| src | `string` | 是 | `''` | 图片源地址 |
| config | `object` | 否 | `{}` | 裁剪配置（aspectRatio、autoCropArea 等） |
| width | `number \| string` | 否 | `'100%'` | 容器宽度 |
| height | `number \| string` | 否 | `'400px'` | 容器高度 |

---

## Events

| 事件名 | 参数 | 说明 |
|---|---|---|
| crop | `object` | 裁剪时触发 |
| ready | `void` | 裁剪器准备就绪时触发 |

---

## AI Usage Rules

1. `src` 为必填项，需提供有效的图片地址。
2. `config` 中的 `aspectRatio` 控制裁剪框宽高比。
3. `crop` 事件在每次裁剪区域变化时触发。
4. `ready` 事件在裁剪器初始化完成后触发，适合做初始化后的操作。
