# useMgUiMsg 组合式函数

> 用于管理框架国际化消息的组合式函数

**版本**: 1.0.0 | **首次引入**: 1.0.0

## 目录

- [基本用法](#基本用法)
- [函数签名](#函数签名)
- [返回值](#返回值)
- [示例](#示例)
- [支持的语言](#支持的语言)

## 基本用法

```typescript
import { useMgUiMsg } from '@magustek/framework-ui'

const { cn, en } = useMgUiMsg()
```

## 函数签名

```typescript
export function useMgUiMsg(): {
  cn: Record<string, string>
  en: Record<string, string>
}
```

## 返回值

| 属性名 | 类型 | 说明 |
|--------|------|------|
| cn | Record<string, string> | 中文消息对象 |
| en | Record<string, string> | 英文消息对象 |

## 示例

### 基础用法

```vue
<template>
  <div>
    <p>{{ cn.add }}</p>
    <p>{{ en.add }}</p>
  </div>
</template>

<script setup lang="ts">
import { useMgUiMsg } from '@magustek/framework-ui'

const { cn, en } = useMgUiMsg()
</script>
```

### 根据语言切换消息

```vue
<template>
  <div>
    <button @click="toggleLanguage">
      {{ currentLanguage === 'cn' ? '切换到英文' : 'Switch to Chinese' }}
    </button>
    <p>{{ messages.add }}</p>
    <p>{{ messages.delete }}</p>
    <p>{{ messages.edit }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMgUiMsg } from '@magustek/framework-ui'

const { cn, en } = useMgUiMsg()
const currentLanguage = ref('cn')

const messages = computed(() => {
  return currentLanguage.value === 'cn' ? cn : en
})

const toggleLanguage = () => {
  currentLanguage.value = currentLanguage.value === 'cn' ? 'en' : 'cn'
}
</script>
```

### 在组件中使用

```vue
<template>
  <div class="toolbar">
    <button @click="handleAdd">{{ messages.add }}</button>
    <button @click="handleEdit">{{ messages.edit }}</button>
    <button @click="handleDelete">{{ messages.delete }}</button>
    <button @click="handleSave">{{ messages.save }}</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useMgUiMsg } from '@magustek/framework-ui'

const { cn, en } = useMgUiMsg()

// 假设从全局状态获取当前语言
const currentLanguage = 'cn'

const messages = computed(() => {
  return currentLanguage === 'cn' ? cn : en
})

const handleAdd = () => {
  console.log('添加')
}

const handleEdit = () => {
  console.log('编辑')
}

const handleDelete = () => {
  console.log('删除')
}

const handleSave = () => {
  console.log('保存')
}
</script>
```

### 获取特定消息

```typescript
import { useMgUiMsg } from '@magustek/framework-ui'

const { cn, en } = useMgUiMsg()

// 获取中文消息
const addButtonText = cn.add        // "添加"
const deleteButtonText = cn.delete  // "删除"
const editButtonText = cn.edit      // "编辑"

// 获取英文消息
const addButtonTextEn = en.add      // "Add"
const deleteButtonTextEn = en.delete // "Delete"
const editButtonTextEn = en.edit    // "Edit"
```

### 与国际化库集成

```vue
<template>
  <div>
    <p>{{ t('add') }}</p>
    <p>{{ t('delete') }}</p>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useMgUiMsg } from '@magustek/framework-ui'

const { locale } = useI18n()
const { cn, en } = useMgUiMsg()

const t = (key: string) => {
  const messages = locale.value === 'zh' ? cn : en
  return messages[key] || key
}
</script>
```

## 支持的语言

- **cn** - 中文（简体）
- **en** - 英文

## 常见消息键

| 键名 | 中文 | 英文 |
|------|------|------|
| add | 添加 | Add |
| delete | 删除 | Delete |
| edit | 编辑 | Edit |
| save | 保存 | Save |
| cancel | 取消 | Cancel |
| confirm | 确认 | Confirm |
| search | 搜索 | Search |
| reset | 重置 | Reset |
| submit | 提交 | Submit |
| close | 关闭 | Close |

## 相关函数

- [useMgIcon](./use-mg-icon.md) - 图标管理函数
- [useSvg](./use-svg.md) - SVG 资源管理函数

## 相关组件

- [MgDialog](../components/mg-dialog.md) - 对话框组件
- [MgSearch](../components/mg-search.md) - 搜索框组件

---

*此文档由 Framework-UI API 文档生成器自动生成*
*最后更新: 2026-02-09*
