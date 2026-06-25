1. 禁止概率补全，缺事实先查真实来源。反例：根据“菜单页”自行生成 API、DTO、权限码、响应结构；正例：先读取 Controller、DTO、组件文档、项目既有代码或向用户确认。
2. 禁止伪造闭环，缺契约就显式阻断或降级。反例：没有新增/编辑路由却写 `router.push({ name: 'MenuEdit' })`；正例：标记为 `blocked-missing-contract`、`example-only`，或先补真实路由文件。
3. 禁止规范背景化，读了规范必须映射到代码规则。反例：读过 `MgToolbar` 文档仍混用 slot 和 `event-handle`；正例：写明“使用 default slot，所以禁止 `@event-handle`”。
4. 禁止未验证事实用确定语气，证据不足必须标注未确认。反例：直接说 `payload.data.list` 是返回结构；正例：按真实 `MgPageResponse<T>` 或后端 DTO 解包，未知时标记待确认。
5. 禁止局部正确放大，必须逐项验证关键链路。反例：组件组合正确就认为整体可交付；正例：逐项检查导入路径、组件 props/events/slots、API 契约、权限来源、路由闭环、typecheck/build。
