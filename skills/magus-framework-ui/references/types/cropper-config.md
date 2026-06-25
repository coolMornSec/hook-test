# CropperConfig

> 图片裁剪器的配置类型定义

## 类型定义

```typescript
interface CropperConfig {
  // 基础配置
  aspectRatio?: number              // 裁剪框的宽高比
  autoCropArea?: number             // 自动裁剪区域的大小（0-1）
  responsive?: boolean              // 是否响应式
  restore?: boolean                 // 是否显示恢复按钮
  guides?: boolean                  // 是否显示参考线
  center?: boolean                  // 是否显示中心指示器
  highlight?: boolean               // 是否高亮裁剪框
  cropBoxMovable?: boolean           // 裁剪框是否可移动
  cropBoxResizable?: boolean         // 裁剪框是否可调整大小
  toggleDragModeOnDblclick?: boolean // 双击切换拖动模式
  
  // 事件回调
  ready?: (e: Event) => void
  cropstart?: (e: Event) => void
  cropmove?: (e: Event) => void
  cropend?: (e: Event) => void
  crop?: (e: Event) => void
  zoom?: (e: Event) => void
}
```

## 属性

| 属性名 | 类型 | 可选 | 说明 |
|--------|------|------|------|
| aspectRatio | number | 是 | 裁剪框的宽高比，例如 16/9 表示 16:9 的比例 |
| autoCropArea | number | 是 | 自动裁剪区域的大小，范围 0-1，默认 0.8 |
| responsive | boolean | 是 | 是否在窗口大小改变时响应式调整 |
| restore | boolean | 是 | 是否显示恢复按钮 |
| guides | boolean | 是 | 是否显示参考线（九宫格） |
| center | boolean | 是 | 是否显示中心指示器 |
| highlight | boolean | 是 | 是否高亮显示裁剪框 |
| cropBoxMovable | boolean | 是 | 裁剪框是否可以移动 |
| cropBoxResizable | boolean | 是 | 裁剪框是否可以调整大小 |
| toggleDragModeOnDblclick | boolean | 是 | 双击时是否切换拖动模式 |
| ready | Function | 是 | 裁剪器准备就绪时的回调函数 |
| cropstart | Function | 是 | 开始裁剪时的回调函数 |
| cropmove | Function | 是 | 裁剪过程中的回调函数 |
| cropend | Function | 是 | 裁剪结束时的回调函数 |
| crop | Function | 是 | 裁剪时的回调函数 |
| zoom | Function | 是 | 缩放时的回调函数 |

## 使用示例

### 基础配置

```typescript
import type { CropperConfig } from '@magustek/framework-ui'

const config: CropperConfig = {
  aspectRatio: 16 / 9,
  autoCropArea: 0.8,
  responsive: true,
  guides: true,
  center: true
}
```

### 完整配置

```typescript
const config: CropperConfig = {
  // 基础配置
  aspectRatio: 1,
  autoCropArea: 0.9,
  responsive: true,
  restore: true,
  guides: true,
  center: true,
  highlight: true,
  cropBoxMovable: true,
  cropBoxResizable: true,
  toggleDragModeOnDblclick: true,
  
  // 事件回调
  ready: (e) => {
    console.log('裁剪器已准备就绪')
  },
  cropstart: (e) => {
    console.log('开始裁剪')
  },
  cropmove: (e) => {
    console.log('正在裁剪')
  },
  cropend: (e) => {
    console.log('裁剪结束')
  },
  crop: (e) => {
    console.log('裁剪数据:', e.detail)
  },
  zoom: (e) => {
    console.log('缩放比例:', e.detail.ratio)
  }
}
```

### 在组件中使用

```vue
<template>
  <MgCropper
    :src="imageSrc"
    :config="cropperConfig"
    @crop="handleCrop"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MgCropper } from '@magustek/framework-ui'
import type { CropperConfig } from '@magustek/framework-ui'

const imageSrc = ref('/path/to/image.jpg')

const cropperConfig: CropperConfig = {
  aspectRatio: 16 / 9,
  autoCropArea: 0.8,
  responsive: true,
  guides: true,
  center: true,
  crop: (e) => {
    console.log('裁剪数据:', e.detail)
  }
}

const handleCrop = (data) => {
  console.log('裁剪完成:', data)
}
</script>
```

## 相关类型

- [CropperRealTimeData](./cropper-real-time-data.md) - 裁剪实时数据类型
- [MgCropper](../components/mg-cropper.md) - 图片裁剪组件

---

*最后更新: 2026-02-09*
