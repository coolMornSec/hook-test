# Framework Core

此文件只记录业务模块开发中常用的 `@magustek/framework-core` 能力。骨架初始化能力只用于识别既有项目，不指导普通模块开发去改全局入口。

## 模块开发常用能力

| 能力 | 用途 | 读取/使用时机 |
|---|---|---|
| `useAxios` | 业务 API 请求 | 新增或调整模块 API 文件 |
| `useDicts` | 获取平台字典 | 字段来自字典 code |
| `useLocale` | 读取/切换语言 | 模块接入 i18n 或验证语言切换 |
| `useCoreStore` | 读取用户、字典、权限等基础数据 | 目标项目已有该模式时复用 |
| `useMultiTags` | 操作标签栏 | 新增/编辑保存后需要关闭或跳转标签 |
| `useKeepAliveTag` | 缓存子应用页面 | 目标项目 layout 已使用 keep-alive 标签 |
| `definePersistStore` / `defineRefStore` | 模块状态 | 多页面共享状态且目标项目已有 store 模式 |
| `useGlobalPinia` / `useGlobalStore` | 全局实例和共享数据 | 微前端或跨模块共享场景 |

## useAxios

业务模块 API 必须通过 `useAxios()`。具体 URL、GET/POST、DTO、分页字段和响应类型规则见 `api-permission-dictionary.md`。

`useAxios()` 的返回数据可能是响应式引用。调用端必须以当前依赖版本和实际类型声明为准，先解包再访问业务字段。推荐使用明确泛型和 `unref`：

```ts
const { data } = await api.page(params)
const payload = unref(data)
rows.value = payload.list ?? []
```

若目标代码库提供统一响应适配函数，优先复用。禁止使用 `(data as any)?.value ?? data` 等同时兼容多种未知结构的写法；这会绕过类型检查并掩盖接口契约错误。

```ts
import { useAxios } from '@magustek/framework-core'

const { get, post } = useAxios()

export const useConfirmedApi = () => ({
  page: (params: ConfirmedPageReq) => post<MgPageResponse<ConfirmedDTO>>('/confirmed-service/resource/page', params),
  detail: (id: string) => get<MgDataResponse<ConfirmedDTO>>(`/confirmed-service/resource/find-by-id/${id}`),
})
```

以上示例只展示调用形态，生成代码必须替换为目标项目真实服务前缀、资源路径和 DTO。
`GET + @RequestParam` 查询对象直接作为 `get(url, params)` 的第二个参数传入，不得包装为 `{ params }`。

## useDicts

通过字典 code 获取字典信息。字典 code、label/value 字段和状态色必须来自需求、接口契约或用户确认。

```ts
import { useDicts } from '@magustek/framework-core'

const statusOptions = useDicts('confirmed_dict_code')
```

字典业务规则见 `api-permission-dictionary.md`。

## useLocale

读取或切换当前语言。模块级 i18n 增量规则见 `i18n-theme.md`。

```ts
import { useLocale } from '@magustek/framework-core'

const { locale } = useLocale()
```

## useCoreStore

读取基础数据。只在目标项目已有该模式时复用，不用它绕过权限、字典或接口契约确认。

```ts
import { useCoreStore } from '@magustek/framework-core'

const { userInfo, dicts, authCodes } = useCoreStore()
```

## useMultiTags / useKeepAliveTag

用于页签和 keep-alive 场景。新增/编辑保存后的返回、关闭和刷新行为优先跟随目标项目已有封装；没有封装时再使用这些能力。

```ts
import { useMultiTags } from '@magustek/framework-core'

const { closeActive, pushTag } = useMultiTags()
```

```ts
import { useKeepAliveTag } from '@magustek/framework-core'

const { keepAliveList, keepAliveComponent } = useKeepAliveTag()
```

## Store 能力

- `definePersistStore`：需要持久化的模块状态。
- `defineRefStore`：响应式模块状态。
- `useGlobalPinia`：微前端或非 setup 场景获取全局 Pinia。
- `useGlobalStore`：目标项目已有共享数据约定时复用。

新增 store 前必须确认目标项目已有 store 分层和命名规范；简单页面局部状态不要上升为全局 store。



## 其他能力

以下能力通常属于骨架初始化或全局入口维护。非必要不做修改：

## `createI18n`

创建国际化实例

```ts
import { createApp } from "vue";
import { createI18n, useLocale } from "@magustek/framework-core";

const app = createApp();
const i18n = createI18n({ locale: useLocale().locale.value });
i18n.withGlobalLocale();
i18n.mergeLocalMessages({ cn: {}, en: {} });

app.use(i18n);
```

## `createRouter`

创建路由实例

```ts
import { createApp } from "vue";
import { createRouter } from "@magustek/framework-core";

const app = createApp();
const router = createRouter({ base: "", routes: [] });

app.use(router);
```

## `createPinia`

创建 pinia 实例

```ts
import { createApp } from "vue";
import { createPinia } from "@magustek/framework-core";

const app = createApp();
const pinia = createPinia({ storage: localStorage });

app.use(pinia);
```

## useToken

获取、设置、删除 token 信息

```javascript
import { useToken } from "@magustek/framework-core";
const { getToken, setToken, removeToken } = useToken();

// 获取 token
const token = getToken();

// 设置 token
setToken(token);

// 删除 token
removeToken();
```

注释中的 token 登录调试示例如需保留空 token，统一写成 `setToken('')`；不得生成空模板字符串 ``setToken(``)``，也不得在生产启用路径中写入或清空调试 token。


## useClearStore

清除 store 缓存信息

```ts
import { useClearStore } from "@magustek/framework-core";

const { clearAll } = useClearStore()

// 清除所有缓存数据
clearAll()
```

## 边界

- 本文件记录 framework-core 能力，不替代业务模块规范。
- `onShow` 已弃用，keep-alive 显示回调使用 `framework-biz-utils` 的 `onShow`。
- 示例中的 URL、DTO、字典 code 和变量名都不是生产契约。
