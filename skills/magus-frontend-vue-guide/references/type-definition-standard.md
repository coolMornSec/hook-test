# Type Definition Standard

本 reference 规定 Magus Vue 业务模块中的 TypeScript 类型落位、命名、职责拆分、转换层和自检要求。核心原则是：先判断类型归属，再决定位置；类型跟随架构边界，不按“看起来整齐”统一堆到 `src/types/`。

## 归属原则

- 局部类型就近定义；共享类型必须有真实复用和稳定语义。
- API 契约类型、领域模型、页面展示模型、表单模型、树模型、详情模型不得混用。
- 类型复用不能以牺牲必填性为代价；禁止为了复用把大量字段改成可选。
- 自动生成类型与手写类型必须隔离，禁止混放。
- `src/types/` 只存跨模块共享基础类型、全局声明和通用工具类型，不存具体业务模块的大量类型。

## 目录落位

新建或重构模块时按下列规则落位；目标项目已有明确同类目录时，优先跟随目标项目，但必须保持相同职责边界。

| 类型类别 | 默认位置 | 说明 |
|---|---|---|
| 手写接口请求、响应、DTO | `src/api/{module}/types.ts` | 与 API 模块同归属；字段必须来自后端 DTO 或已确认 `apiContractContext` |
| 自动生成接口类型 | `src/types/generated/` 或 `src/api/generated/` | 由 OpenAPI、schema、后端导出等生成；禁止手改和手写类型混放 |
| 业务领域模型 | `src/modules/{module}/types/domain.ts` | 表达前端业务概念和稳定规则；没有 `src/modules` 的页面内聚项目放在页面模块 `types/domain.ts` |
| 页面展示模型 | `src/modules/{module}/types/view.ts` | 表格行、树节点、详情展示、看板卡片等 UI 展示结构 |
| 表单模型 | `src/modules/{module}/types/form.ts` | 新增、编辑、查询表单的交互结构和校验状态 |
| 组件私有类型 | 组件文件内或组件目录 `types.ts` | Props、Emits、Slots、Expose、局部 option、局部 row 等 |
| 跨模块共享基础类型 | `src/types/` 或 `src/shared/types/` | 例如分页基础类型、通用树节点、通用 option；不得包含具体业务字段 |
| 通用工具类型 | `src/types/utility.ts` | 例如 `Nullable<T>`、`ValueOf<T>`、`DeepPartial<T>` |
| 全局声明 | `src/types/*.d.ts` | 环境变量、第三方库扩展、全局类型声明 |

页面内聚项目如果没有 `src/modules`，可使用：

```text
src/pages/[relative-module]/
  types/
    domain.ts
    view.ts
    form.ts
  mapper.ts
```

老项目增量修改时，不为了本规范做大规模搬迁；但新增类型必须放在正确归属位置，且不得继续扩大 `src/types/` 的业务类型堆积。

## 命名规范

类型名称必须表达业务职责，不使用空泛后缀兜底。

推荐：

```ts
export interface UserListQuery {}
export interface UserListResponse {}
export interface UserDTO {}
export interface UserDomain {}
export interface UserTableRow {}
export interface UserDetailView {}
export interface UserFormModel {}
export interface UserSearchForm {}
export interface UserTreeNode {}

export type UserStatus = 'enabled' | 'disabled'
export type UserId = string
```

禁止：

```ts
export interface UserType {}
export interface UserData {}
export interface UserInfo {}
export interface FormType {}
export interface TableData {}
export interface Item {}
```

后端已有 DTO / VO / Query / Command 命名体系时，前端 API 契约类型可以保持同名或可追踪命名；同一模块内不得混用多套后缀体系，例如同时出现 `UserVO`、`UserResponse`、`UserResult` 表示同一响应。

## 职责拆分

同一字段结构相似不代表可以共用同一类型。不同变化原因必须拆开：

- 接口响应变化影响 DTO。
- 表单校验和交互变化影响 `FormModel`。
- 表格列、状态色、展示文案变化影响 `TableRow` 或 `View`。
- 领域规则变化影响 `Domain`。

禁止一个类型同时承担：

- 接口响应和表单提交。
- 表单模型和表格行。
- 树节点和详情展示。
- 请求查询和页面搜索状态。
- DTO 和领域模型。

## Mapper 规则

只要 DTO 与页面展示、表单或领域模型不完全等价，就必须提供转换层。

默认位置：

```text
src/modules/{module}/mapper.ts
```

页面内聚项目：

```text
src/pages/[relative-module]/mapper.ts
```

示例：

```ts
import type { UserDTO } from '@/api/user/types'
import type { UserFormModel } from './types/form'
import type { UserTableRow } from './types/view'

export const toUserTableRow = (dto: UserDTO): UserTableRow => ({
  id: dto.id,
  name: dto.name,
  status: dto.status,
})

export const toUserFormModel = (dto: UserDTO): UserFormModel => ({
  id: dto.id,
  name: dto.name,
  status: dto.status,
})
```

转换函数必须命名为 `to{Target}`、`from{Source}` 或目标项目已有等价风格。禁止在页面模板、表格列 formatter、表单提交函数中散落大段 DTO 字段适配逻辑。

## 导入导出

- 类型导入必须使用 `import type`。
- 默认使用命名导出，不为类型创建默认导出。
- 谨慎使用 `export *`；跨模块 barrel export 会模糊依赖边界，只有目标项目已有清晰出口规范时才沿用。
- 禁止通过全局声明暴露业务类型。

## 动态数据

- 禁止裸 `any`。
- 外部未知数据使用 `unknown`，并通过类型守卫、schema 解析、适配层或明确泛型收窄。
- 禁止用 `unknown as Xxx`、`as any` 或多层可选链掩盖接口契约缺失。
- 非空断言只能用于框架生命周期已保证的场景，并应优先用显式判断替代。

## AI 生成步骤

生成类型前必须按顺序执行：

1. 从需求、后端 DTO、`apiContractContext`、既有同类模块中识别类型来源。
2. 为每个类型标注类别：API 契约、生成类型、领域模型、展示模型、表单模型、组件私有类型、共享基础类型。
3. 按类别选择落位；缺目录时创建最近归属目录，不默认写入 `src/types/`。
4. 为 DTO 到领域、展示、表单的差异建立 `mapper.ts`。
5. 在 API、页面、组件、composable 中使用 `import type` 引入类型。
6. 运行类型检查或记录环境阻断。

## 类型检查项

生成后必须自检：

- 是否存在具体业务类型落入 `src/types/`。
- 是否存在自动生成类型和手写类型混放。
- 是否 API 请求、响应、DTO 类型没有放在 API 模块归属位置。
- 是否领域、展示、表单类型缺少分层或命名无法表达职责。
- 是否一个类型被响应、表单、表格、树、详情多个场景共用。
- 是否为了复用把大量字段定义为可选。
- 是否 DTO 到展示模型、表单模型、详情模型的转换缺少 `mapper.ts` 或等价适配层。
- 是否存在裸 `any`、`as any`、`unknown as`、滥用非空断言或禁用 lint。
- 是否类型导入缺少 `import type`。
- 是否新增字段、枚举、必填项与后端 DTO 或已确认契约不一致。

推荐验证：

```bash
vue-tsc --noEmit
```

若目标项目没有 `vue-tsc`，执行项目等价 typecheck 或 build；无法执行时必须说明阻断原因、已做的静态检查和残余风险。
