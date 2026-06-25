# CropperRealTimeData 类型

> 图片裁剪器实时数据类型定义

**版本**: 1.0.0 | **首次引入**: 1.0.0

## 类型定义

```typescript
export type CropperRealTimeData = {
  x: number
  y: number
  width: number
  height: number
  rotate: number
  scaleX: number
  scaleY: number
}
```

## 属性说明

| 属性名 | 类型 | 说明 |
|--------|------|------|
| x | number | 裁剪框距离左边的距离（像素） |
| y | number | 裁剪框距离顶部的距离（像素） |
| width | number | 裁剪框的宽度（像素） |
| height | number | 裁剪框的高度（像素） |
| rotate | number | 图片旋转角度（度数） |
| scaleX | number | 图片水平缩放比例 |
| scaleY | number | 图片垂直缩放比例 |

## 使用示例

### 基础用法

```typescript
import type { CropperRealTimeData } from '@magustek/framework-ui'

const cropData: CropperRealTimeData = {
  x: 0,
  y: 0,
  width: 300,
  height: 300,
  rotate: 0,
  scaleX: 1,
  scaleY: 1
}
```

### 在组件中使用

```vue
<template>
  <MgCropper
    :src="imageSrc"
    @crop="handleCrop"
  />
</template>

<script setup lang="ts">
import type { CropperRealTimeData } from '@magustek/framework-ui'
import { MgCropper } from '@magustek/framework-ui'

const imageSrc = ref('')

const handleCrop = (data: CropperRealTimeData) => {
  console.log('裁剪数据:', data)
  console.log('裁剪框位置:', { x: data.x, y: data.y })
  console.log('裁剪框大小:', { width: data.width, height: data.height })
  console.log('图片变换:', { rotate: data.rotate, scaleX: data.scaleX, scaleY: data.scaleY })
}
</script>
```

### 获取裁剪结果

```typescript
const cropData: CropperRealTimeData = {
  x: 50,
  y: 50,
  width: 200,
  height: 200,
  rotate: 45,
  scaleX: 1.2,
  scaleY: 1.2
}

// 使用裁剪数据生成图片
const canvas = document.createElement('canvas')
canvas.width = cropData.width
canvas.height = cropData.height
// ... 绘制裁剪后的图片
```

## 相关类型

- [CropperConfig](./cropper-config.md) - 裁剪器配置类型

## 相关组件

- [MgCropper](../components/mg-cropper.md) - 图片裁剪组件

---

*此文档由 Framework-UI API 文档生成器自动生成*
*最后更新: 2026-02-09*
