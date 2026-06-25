# Framework Biz Utils

此文件只记录业务模块开发中常用的 `@magustek/framework-biz-utils` 方法签名和使用边界。

## 使用原则

- 目标项目已经安装并使用 `@magustek/framework-biz-utils` 时优先复用。
- 未安装时不要为了单个页面强行新增依赖，先跟随目标项目已有返回、页签和下载封装。
- `onShow`、`watchInComponent` 适合 keep-alive 页签场景；普通组件优先使用 Vue 原生生命周期和 watch。
- 示例只展示调用形态，生成代码必须替换为目标项目真实路由、应用 code、文件 id、模板 code 和接口契约。

## closeAndToNext

关闭当前激活标签并跳转到下一个标签。

```ts
function closeAndToNext(next?: RouteLocationRaw, appName?: string): void
```

| 参数名 | 类型 | 说明 |
|---|---|---|
| `next` | `RouteLocationRaw` | 非必传；若传入，作为下一个标签跳转目标 |
| `appName` | `string` | 传入 `next` 时需要同时传应用 code |

```ts
import { closeAndToNext } from '@magustek/framework-biz-utils'

closeAndToNext()
```

## backToLast

返回上一次页面。

```ts
function backToLast(last?: RouteLocationRaw, appName?: string): void
```

| 参数名 | 类型 | 说明 |
|---|---|---|
| `last` | `RouteLocationRaw` | 非必传；若传入，作为返回目标 |
| `appName` | `string` | 传入 `last` 时需要同时传应用 code |

```ts
import { backToLast } from '@magustek/framework-biz-utils'

backToLast()
```

## onShow

在 keep-alive 组件显示时触发。

```ts
function onShow(callback: Function): void
```

```ts
import { onShow } from '@magustek/framework-biz-utils'

onShow(() => {
  // refresh current page data
})
```

## watchInComponent

类似 Vue 的 `watch`，但只在组件激活时工作，组件失活或销毁会停止 watch。

```ts
import { watchInComponent } from '@magustek/framework-biz-utils'

watchInComponent(
  () => route.query,
  () => {
    // sync active page data
  },
)
```

## download

根据文件 id 获取文件完整链接，或者下载文件。

```ts
function download(
  fileId: string,
  download?: boolean,
  config?: { path?: string; fileName?: string }
): Promise<{ url: string; name: string }>
```

## downloadTemplate

下载模板文件管理中的文件。

```ts
function downloadTemplate(
  templateData: { appCode: string; code: string },
  config?: { path?: string; fileName?: string }
): Promise<{ url: string; name: string }>
```

