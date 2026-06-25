# API, Permission, and Dictionary

此文件只描述业务模块中的 API、权限和字典/枚举规则。

## API

- API 必须基于 `@magustek/framework-core` 的 `useAxios()`。
- 先跟随目标项目既有 API 组织方式：默认导出对象或 `useXxxApi()` 组合函数二选一，不在同一模块混用。
- 服务前缀必须来自后端 `serviceName` 或 `spring.application.name`，二者应一致；缺失或不一致时先确认，不得按模块名、页面名或包名猜测。
- 前端最终发出的后端业务请求必须包含网关路由段，格式为 `/api/{spring.application.name}/{controllerPath}`。例如后端服务 `magus-system` 的 Controller 路径 `/system/menu`，浏览器实际请求必须是 `/api/magus-system/system/menu`。
- 使用 `useAxios()` 且目标项目默认已注入 `/api` 时，API 文件中的 URL 不再手写 `/api`，但必须以 `/{spring.application.name}` 开头，例如 `const url = '/magus-system/system/menu'`；最终请求由 `useAxios` 形成 `/api/magus-system/system/menu`。
- Controller 路径必须来自后端实际代码或共享 `apiContractContext`：类级 `@RequestMapping` + 方法级 `@GetMapping` / `@PostMapping`。设计文档只写接口名称时，必须先补齐固定路径字符串，不得把 `/plan/page` 自行推演成 `/plan-page` 或其他风格。
- 若目标项目使用原生 `fetch`、独立 `axios` 实例或其他不会自动注入 `/api` 的请求封装，代码中的 URL 必须直接包含 `/api/{spring.application.name}`。
- URL 不得只写网关根前缀 `/api`、不得省略服务名、不得写完整域名、页面相对路径或模板地址。
- 新增业务请求默认只解构 `get`、`post`；创建、更新、删除、批量删除也使用 `post`，除非接口契约和目标项目明确不同。
- 请求方法和参数位置必须严格匹配后端 Controller 契约：`GET + @RequestParam` 使用平铺查询参数，`POST + @RequestBody` 使用请求体；不得因为页面是分页查询就统一生成 `post`。
- 使用 `useAxios().get` 调用 `GET + @RequestParam` 接口时，查询对象直接作为第二个参数传入，例如 `get(url, params)`；不得再次包装为 `{ params }`，否则可能生成 `params[page]`、`params[size]` 等后端无法绑定的参数名。只有目标项目真实请求封装明确要求包装时才允许例外，并记录依据。
- `GET + @RequestParam` 的前端字段名必须与后端参数名逐项一致。禁止自行生成后端未声明的 `keyword`、嵌套 `params` 或通用搜索字段；发送前应移除空字符串、`null`、`undefined` 等无意义可选条件，分页必填字段除外。
- 泛型优先使用 `MgPageResponse<T>`、`MgDataResponse<T>`、`MgListResponse<T>`、`MgBaseResponse`。
- DTO/Req/Rsp 类型与后端契约同名或可追踪，默认定义在 `src/api/{module}/types.ts`；字段必须来自后端 DTO 清单，包含字段名、类型、必填项、枚举/状态值和分页字段。字段已知时禁止裸 `any`，不得按页面文案替换后端字段名，也不得补出后端未声明字段。类型落位、命名、职责拆分和 mapper 细则见 `type-definition-standard.md`。
- 分页默认请求字段是 `page`、`size`；响应列表字段和总数字段必须以目标项目真实 `MgPageResponse` 或既有页面为准，常见总数字段为 `total`。
- 下载/导出优先使用 `framework-biz-utils` 的下载工具或项目已有封装。

以下示例只展示调用形态，生成代码必须替换为目标项目真实 URL、DTO、字段和方法名：

```ts
import { useAxios } from '@magustek/framework-core'

const url = '/confirmed-service/confirmed-controller-path'
const { get, post } = useAxios()

export default {
  page: (params: ConfirmedPageReq) => post<MgPageResponse<ConfirmedDTO>>(`${url}/page`, params),
  findOne: (id: string) => get<MgDataResponse<ConfirmedDTO>>(`${url}/find-by-id/${id}`),
  create: (data: ConfirmedSaveReq) => post<MgBaseResponse>(`${url}/create`, data),
  update: (data: ConfirmedSaveReq) => post<MgBaseResponse>(`${url}/update`, data),
  delete: (ids: string[]) => post<MgBaseResponse>(`${url}/delete`, ids),
}
```

组合式 API 只在目标项目已有该模式时使用：

```ts
export const useConfirmedApi = () => {
  const { get, post } = useAxios()
  const url = '/confirmed-service/confirmed-controller-path'

  return {
    page: (params: ConfirmedPageReq) => post<MgPageResponse<ConfirmedDTO>>(`${url}/page`, params),
    detail: (id: string) => get<MgDataResponse<ConfirmedDTO>>(`${url}/find-by-id/${id}`),
  }
}
```

## 权限

- 按钮、批量操作、导出、删除、启停、授权等敏感动作必须加 `v-auth="['权限码']"`。
- 权限码必须来自需求、设计、后端契约、菜单资源表或用户确认，不自行拼接。
- 多权限数组的 and/or 语义以目标项目 `v-auth` 指令实现为准。
- 组件级展示可用 `MgAuth`、`useAuth` 或项目已有封装，但按钮级仍优先 `v-auth`。
- 本技能只消费既有权限码，不设计平台权限模型、权限码体系或角色授权流程。

## 字典与枚举

- 平台字典优先 `useDicts`、`MgDict`、字典选择组件或项目已有封装。
- 用户、部门、职务、工作组、资源选择优先 `MgComplexSelect`、`MgResourceSelect` 或项目已有 Biz 选择器。
- 列表 formatter 不应每行请求字典；字典应在页面级或 store 级缓存。
- 枚举值来自接口契约或字典 code；缺少 code、label、value、状态色时先确认。
- 字典展示文案如果启用 i18n，按 `i18n-theme.md` 接入语言 key；本文件不定义语言包结构。

## 交互要求

- 删除、批量删除、启停、取消授权、重置密码等影响数据的 API 调用前必须确认。
- 项目已有 `useConfirm` 或统一确认封装时优先使用；否则使用 Element Plus `ElMessageBox.confirm`。
- 成功提示和失败恢复按目标项目已有消息封装处理；未确认时使用 Element Plus 消息能力。

## 自检

- API 是否有真实服务前缀和可追踪 DTO。
- API 最终请求是否为 `/api/{spring.application.name}/{controllerPath}`；使用 `useAxios()` 时，代码 URL 是否以 `/{spring.application.name}` 开头且没有重复写 `/api`。
- API 路径是否逐条对照 Controller 实际映射或共享 `apiContractContext`，没有根据接口名称、RESTful 习惯或 kebab-case 推演。
- 请求方法和参数位置是否与 Controller 的 `@GetMapping` / `@PostMapping`、`@RequestParam` / `@RequestBody` 一致。
- Req/Rsp 字段名、类型、必填项、枚举/状态值和分页字段是否与后端 DTO 清单一致。
- `GET + @RequestParam` 是否传递平铺参数，浏览器实际查询串中没有 `params[page]`、`params[size]` 或后端未声明字段。
- 写操作是否使用 `post`，没有误用完整域名。
- 分页请求字段和响应字段是否与后端真实契约匹配。
- 权限码是否全量覆盖敏感动作。
- 字典是否复用缓存或组件，没有重复请求。
- 示例地址、示例 DTO、示例权限码没有进入生产代码。

## 边界

- 不在本文件定义页面结构、表单分层或列表状态，见 `module-development-standard.md`。
- 不在本文件定义类型落位、命名和 mapper 细则，见 `type-definition-standard.md`。
- 不在本文件定义主题和 i18n 接入方式，见 `i18n-theme.md`。
- 不在本文件定义组件 props/events/slots，见 `magus-framework-ui.md`。
