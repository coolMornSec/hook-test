# 类型定义

> Framework-UI 提供的 TypeScript 类型定义

## 📋 类型列表

### 配置类型

- **[CropperConfig](./cropper-config.md)** - 图片裁剪器配置类型
- **[CropperRealTimeData](./cropper-real-time-data.md)** - 图片裁剪实时数据类型
- **[TreePropType](./tree-prop-type.md)** - 树形组件属性类型

## 🚀 快速开始

### 导入类型

```typescript
import type { CropperConfig, TreePropType } from '@magustek/framework-ui'
```

### 在代码中使用

```typescript
const cropperConfig: CropperConfig = {
  aspectRatio: 16 / 9,
  autoCropArea: 0.8,
  responsive: true
}

const treeProps: TreePropType = {
  children: 'children',
  label: 'text',
  disabled: 'disabled'
}
```

## 📖 常用类型

### CropperConfig

图片裁剪器的配置对象类型。

```typescript
interface CropperConfig {
  aspectRatio?: number
  autoCropArea?: number
  responsive?: boolean
  // ... 更多配置项
}
```

### TreePropType

树形组件的属性映射类型。

```typescript
interface TreePropType {
  children: string
  label: string
  disabled: string
}
```

### CropperRealTimeData

图片裁剪的实时数据类型。

```typescript
interface CropperRealTimeData {
  x: number
  y: number
  width: number
  height: number
  rotate: number
  scaleX: number
  scaleY: number
}
```

## 🎯 最佳实践

1. **使用 type 导入** - 使用 `import type` 导入类型，避免运行时开销
2. **类型检查** - 在 TypeScript 中启用严格模式以获得更好的类型检查
3. **扩展类型** - 可以通过 `extends` 关键字扩展现有类型
4. **泛型类型** - 使用泛型类型提高代码的灵活性和可重用性

## 📚 更多资源

- [TypeScript 官方文档](https://www.typescriptlang.org/docs/)
- [Vue 3 TypeScript 支持](https://vuejs.org/guide/typescript/overview.html)

---

*此文档由 Framework-UI API 文档生成器自动生成*
*最后更新: 2026-02-09*
