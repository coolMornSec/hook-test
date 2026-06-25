---
name: magus-frontend-architecture
description: Use during requirements analysis, functional design, implementation planning, document review, or development when creating a new Magus frontend project, initializing a Vue 3 micro-frontend skeleton, or configuring frontend code root directory, Vite base, dev port, proxy, backend gateway URL, package name, mount element, npm registry, or VITE_APP_FRAME micro-frontend layout configuration.
---

# Magus Frontend Architecture

## 定位

本技能负责创建 Magus 前端新项目或初始化 Vue 微前端骨架。需求确认、功能设计、实施计划和文档评审中，只要涉及新建前端项目、全新前端骨架或初始化配置，也必须使用本技能记录初始化约束和配置候选；实际缺失、冲突或不可追溯配置仍由开发前配置确认关卡确认。业务页面、组件、API 调用、权限、字典、主题和 i18n 增量开发继续使用 `magus-frontend-vue-guide` 和 `magus-framework-ui`。

## 输入与输出边界

- 适用条件：新建 Magus Vue 前端项目、初始化微前端骨架，或确定 Vite base、端口、代理、挂载节点和默认 layout。
- 必要输入：7 项前端配置、模板地址/ref、目标目录覆盖策略、Node/pnpm 环境、私服配置和已确认路由约束。
- 标准输出：模板生成的项目骨架、环境文件、Vite/路由/i18n/挂载配置、生成清单和 install/typecheck/build 证据。
- 不负责：业务页面和 API 细节、权限模型设计、正式浏览器功能验收、绕过模板自行发明项目结构。

## 门禁

- 初始化必须通过 `scripts/init-skeleton.mjs` 从模板生成；不得手工新建骨架文件、复制片段或跳过模板仓库。
- 真实项目文件来自 `--template` 指向的可运行模板项目；本技能和脚本只定义确认变量、渲染锚点、复制边界和验证要求。
- 默认模板为 `https://dev.magustek.com/bigdata/magus-basic-platform/magus-ai/magus-init-skeleton.git`，默认 `--ref dev`。生产初始化建议显式指定稳定 tag 或 commit。
- 本地模板只允许在用户明确说明离线调试或模板维护时使用。
- 脚本生成后才能安装依赖、启动开发服务、类型检查或构建；缺少 `.npmrc` 时不得安装依赖。
- `init-skeleton` 是技能内脚本命令，不是 自动注册的 slash command。

## <HARD-GATE>开发前配置确认

新骨架初始化前必须确认 7 项配置。先从用户原始需求、服务名、已确认文档、阶段交接物、project-memory、目标目录命名和同类项目配置中推导推荐值；能追溯来源的值直接记录，不重复提问。多个已有推荐值的配置合并为一次差异确认，用户只覆盖差异项；未展示的值不得视为默认同意。

| 配置项 | 用途 | 推荐值推导 |
|---|---|---|
| `packageName` | `package.json` 的 `name`、`index.html` 标题 | 默认 `magus-framework-<module>`；同类项目已有包名前缀时优先沿用 |
| `frontendRootDir` | 目标项目目录 | 默认当前工作区下 `{serviceName}-ui`；文档已指定时用文档路径 |
| `VITE_APP_BASE` / `--base` | 微前端模块部署路由前缀、Vite `base`、路由 history base、构建输出目录 | 微前端部署必须有值；按用户指定、已确认文档、模块名/菜单一级入口、`spring.application.name` 去前缀短名、前端项目名去 `-ui` 后缀依次推导；只填写路由值本身，不含首尾 `/` |
| `VITE_APP_PORT` / `--port` | Vite dev server 端口 | 只能来自端口规划、同类项目、文档或用户输入；不能猜测 |
| `VITE_APP_SERVER_URL` / `--serverUrl` | `/api` 代理目标 | 已确认的后端网关服务地址 |
| `VITE_APP_FRAME` / `--frame` | 微前端开发布局 | 默认推荐 `YES`；生产环境脚本固定写 `NO` |
| `mountElementId` | `index.html` 根节点、`main.ts` 挂载选择器、根样式选择器 | 默认 `app`或者`magus-<module>` |

`module` 优先取业务一级入口或后端 `spring.application.name` 去掉组织/框架前缀后的稳定短名；不得使用临时中文名、随机缩写或模板默认名。

缺失项提问必须带推荐值和来源，例如：

```text
仍缺少 2 项初始化配置：
1. VITE_APP_PORT：未在文档、同类项目或端口规划中找到；请确认开发端口。
2. VITE_APP_SERVER_URL：推荐使用 <已发现网关地址>，来源 <文件/文档/上下文>；请确认是否采用。
```

## init-skeleton命令

执行前必须已有配置确认记录。确认记录缺失时，先回到“配置问答推导与确认”，不得用推荐值、占位符或“后续再改”替代确认。

```bash
node skills/magus-frontend-architecture/scripts/init-skeleton.mjs \
  --template https://dev.magustek.com/bigdata/magus-basic-platform/magus-ai/magus-init-skeleton.git \
  --ref dev \
  --target <前端代码根目录> \
  --packageName <前端应用包名> \
  --base <VITE_APP_BASE> \
  --port <VITE_APP_PORT> \
  --serverUrl <VITE_APP_SERVER_URL> \
  --frame <YES|NO> \
  --mountElementId <DOM挂载节点ID>
```

可选参数：

```bash
--template <Git仓库URL或本地模板目录>
--ref <Git分支、tag或commit>
--force
--dry-run
```

- `--dry-run` 只下载或读取模板、在内存中渲染并执行静态校验，不写入目标目录。正式生成前必须先 dry-run。
- `--force` 只在用户明确允许覆盖目标目录同名文件时使用。未使用 `--force` 时，脚本遇到同名文件必须停止。
- `--base` 表示微前端模块部署路由前缀，微前端部署禁止为空；非空值不得以 `/` 开头或结尾。只有用户明确声明非微前端站点根部署时才允许空值，并必须在确认记录中写明例外来源。
- 脚本只负责生成和静态校验，不执行 `pnpm install`、`pnpm typecheck` 或 `pnpm build`。

## 模板文件生成边界与变量替换

生成初始化骨架文件禁止保留 `{{...}}` 占位符；脚本基于真实默认锚点和配置文件渲染。

| 文件或目录 | 生成方式 | 必须检查 |
|---|---|---|
| `package.json` | 从模板复制后改写 | `name` 等于 `packageName`； |
| `index.html` | 从模板复制后改写 | `<title>` 等于 `packageName`，根节点 id 等于 `mountElementId` |
| `.env`、`.env.development` | 脚本按确认值重写 | `VITE_APP_BASE`、`VITE_APP_PORT`、`VITE_APP_SERVER_URL`、`VITE_APP_FRAME` 与确认值一致 |
| `.env.production` | 脚本按确认值重写 | `VITE_APP_FRAME=NO`，其他 Vite 变量与确认值一致 |
| `.npmrc` | 从模板复制 | 必须包含 `@magustek:registry` |
| `src/main.ts` | 从模板复制后替换挂载选择器 | 使用 `app.mount('#<mountElementId>')` |
| `src/styles/index.scss` | 从模板复制后替换根选择器 | 包含 `#<mountElementId>`，保证根高度和样式生效 |
| `vite.config.ts` | 从模板复制 | 保留 Vite base、代理、文件式路由根配置、自动导入和 resolver 配置 |
| `src/pages`、`src/router`、`src/lang`、`src/App.vue`、`src/vite-env.d.ts` | 从模板复制 | 作为骨架能力入口保留，业务页面开发按 `magus-frontend-vue-guide` |
| `auto-imports.d.ts`、`components.d.ts`、`router-map.d.ts`、`.eslintrc-auto-import.json` | 不复制 | 由 Vite 插件、类型检查或开发服务生成 |

脚本排除 `.git`、`node_modules`、`dist`、`dist-ssr`、缓存目录和自动生成声明文件。目标文件中不得残留 `{{...}}` 占位符。

骨架基线：

- Vue 3 + TypeScript + Vite。
- 文件式路由：`src/pages` + `vue-router/vite` + `vue-router/auto-routes`；业务页面按设计阶段 `menuPageContext.frontend.menuFilePath` 落位。
- `vite.config.ts` 保留文件式路由插件配置；`VITE_APP_BASE` 只表示微应用部署前缀。
- 自动导入：`VueRouterAutoImports` 必须进入 `AutoImport.imports`。
- Vite base、dev port、proxy target 来自 `.env*`。
- i18n 合并 `useMgUiMsg()`、`useBizUiMsg()` 和 Element Plus locale。
- 默认页保留 `defineOptions({ name: 'IndexPage' })` 和 `definePage(...)`。

## 生成顺序

1. 推导 7 项配置推荐值，记录“配置项 -> 推荐值 -> 来源 -> 是否仍需确认”。
2. 向用户确认推荐值和缺失、冲突或不可追溯项。
3. 确认目标目录和覆盖策略；目标目录已有同名文件且用户未允许覆盖时，不得使用 `--force`。
4. 执行 `init-skeleton --dry-run`，验证模板可下载、必需文件存在、变量可渲染、目标内容无占位符残留。
5. dry-run 通过后执行正式 `init-skeleton`。
6. 检查目标目录中的 `.npmrc` 后安装依赖。
7. 运行 `pnpm typecheck`；若因自动生成声明文件缺失失败，短暂启动 Vite 开发服务生成 `auto-imports.d.ts`、`components.d.ts`、`router-map.d.ts`，停止服务后重跑 typecheck。
8. 运行 `pnpm build`，项目要求 lint/test 时继续运行对应命令。
9. 记录所有命令、退出码和关键输出。

- `vite.config.ts` 使用 `loadEnv(mode, process.cwd(), '')` 读取 `VITE_APP_BASE`、`VITE_APP_PORT`、`VITE_APP_SERVER_URL`。
- `VITE_APP_BASE` 只保存微前端模块部署路由值本身，微前端部署禁止为空，非空值不得以 `/` 开头或结尾；格式不合法时必须先修正确认记录再生成，不得原样写入 `.env*`。
- `vite.config.ts` 必须注册 `VueRouter(...)`，并把 `VueRouterAutoImports` 放入 `AutoImport.imports`，保证 `src/pages`、`definePage` 和文件式路由类型生成可用。
- `VITE_APP_BASE` 是微应用部署前缀，不参与业务路由建模。业务路由来自设计阶段 `menuPageContext.frontend.routePath`；公开访问路径仅作为前端派生验证值：`frontend.publicAccessPath=join("/", frontend.VITE_APP_BASE, frontend.routePath)`。后端只消费 `menuPageContext.backend.appGroupInfoPage`，不得从前端变量补业务段。
- Vite `base` 必须为 `/${base}/`，build 输出必须为 `dist/${base}`。
- dev server 端口来自 `Number(env.VITE_APP_PORT)`；`server.open` 使用 `frontend.publicAccessPath` 或其派生值；代理 `/api` 到 `serverUrl`，并去掉 `/api` 前缀。
- `router/index.ts` 使用 `createWebHistory(import.meta.env.BASE_URL)`，不得改回手写 `createRouter({ base: import.meta.env.VITE_APP_BASE })`。
- `src/lang/index.ts` 必须合并 `useMgUiMsg()` 和 `useBizUiMsg()`，保证 Magus 组件国际化正常显示。
- 若目标项目作为 wujie 子应用、shadow DOM 子应用或多 Document 微前端运行，`src/main.ts` 必须包含 `document.adoptedStyleSheets` setter 兼容修补；不得引入会在模块加载阶段跨 Document 共享 constructed stylesheet 的组件包装层。
- `src/App.vue` 必须使用 `ElConfigProvider` 和 `useLocale()` 派生 Element Plus 语言包。
- 自动导入和组件解析必须保留 Element Plus、VueUse、Icons、Magus UI/Biz UI resolver。
- `src/vite-env.d.ts` 必须声明 `VITE_APP_BASE`、`VITE_APP_PORT`、`VITE_APP_SERVER_URL`。
- 默认首页必须保留 `defineOptions({ name: 'IndexPage' })` 和 `definePage(...)`，保证文件式路由类型生成可用。
- 文件式路由菜单页面必须按 `menuPageContext.frontend.menuFilePath` 落位，并证明 `frontend.routePath` 等于 `menuPageContext.common.finalMenuPath`。
- 不生成 `auto-imports.d.ts`、`.eslintrc-auto-import.json`、`components.d.ts`、`router-map.d.ts`；这些文件由 Vite 插件、类型检查或开发服务自动生成。
- 基于骨架生成的初始化代码需要保留模板中的注释和注释代码
- 保留模板中的注释代码时，仍必须检查 TypeScript 语法和目标项目格式规范。token 登录调试示例中的空 token 统一写为 `setToken('')`，不得生成空模板字符串 ``setToken(``)``，也不得在生产启用路径中写入、清空或覆盖调试 token。
- 不得把新前端骨架降级为 `src/view` + 手写 `src/router` 业务路由表；只有既有前端项目增量开发才允许跟随其手写路由模式。

## 验证与失败处理

初始化后至少验证：

```bash
pnpm install
pnpm typecheck
pnpm build
```

项目要求 lint 时再运行：

```bash
pnpm lint
```

必要检查项：

- dry-run 通过，正式生成使用同一组确认变量。
- 目标目录存在 `package.json`、`.npmrc`、`.env*`、`index.html`、`src/main.ts`、`src/styles/index.scss`、`vite.config.ts`。
- `.env*` 中 `VITE_APP_BASE` 对微前端部署必须非空且不含首尾 `/`；生产环境 `VITE_APP_FRAME=NO`。
- `index.html` 根节点、`src/main.ts` 挂载选择器和 `src/styles/index.scss` 根选择器一致。
- `vite.config.ts` 保留 `vue-router/vite`、`vue-router/unplugin`、`VueRouter(...)` 和 `VueRouterAutoImports`；`src/router/index.ts` 使用 `import.meta.env.BASE_URL`。
- 公开访问路径与 `menuPageContext.frontend.publicAccessPath` 或派生公式一致。
- `.npmrc` 包含 `@magustek:registry`。

失败处理：

- 模板无法下载、认证失败或 ref 不存在：停止并记录模板 URL、ref、命令和错误输出，不要改用本地模板。
- 目标目录已有文件：停止并列出冲突文件；只有用户明确允许覆盖后才可使用 `--force`。
- 依赖安装失败：记录 registry、`.npmrc` 状态、Node/pnpm 版本和错误输出。
- typecheck 因自动导入声明缺失失败：启动 Vite 一次生成声明文件后复验。
- 无法完成安装、typecheck 或 build：不得声明骨架可运行，只能说明已生成文件和剩余风险。

## 常见错误

- 只确认后端网关地址，漏掉 `VITE_APP_BASE`、端口或挂载节点；或在微前端部署下把 `VITE_APP_BASE` 推荐为空。
- 把含首尾 `/` 的访问路径原样写入 `VITE_APP_BASE`，导致 Vite 再次拼接 `/`。
- 把 `.env` 占位符当作用户确认记录。
- 未确认挂载节点就写死模板中的默认选择器。
- 运行时复制外部示例目录，导致技能离开当前仓库后不可用。
- 安装依赖前没有 `.npmrc`，导致 `@magustek/*` 依赖无法解析。
- 忘记同步修改 `src/styles/index.scss` 的根选择器，页面高度失效。
- 删除 i18n 合并逻辑，导致 Magus UI 或 Biz UI 文案显示异常。
- 文件式路由缺少 `vue-router/vite` 或 `VueRouterAutoImports`，导致生成页面、`definePage` 或路由类型不可用。
- 混淆 `VITE_APP_BASE` 和业务路由：把微应用部署前缀写进 `menuPageContext.frontend.routePath`、页面文件路径或 `@AppGroupInfo.page`。
- wujie 子应用中漏掉 `document.adoptedStyleSheets` setter 修补，或在模块加载阶段引入会写入 constructed stylesheet 的包装组件。
- 原样保留模板中的错误 token 调试片段，例如空模板字符串 ``setToken(``)``。
- 绕过 `init-skeleton` 手工创建骨架，导致模板文件、`.npmrc`、自动导入、i18n 或根样式缺失。
- 只确认后端网关地址，漏掉 `VITE_APP_BASE`、端口、`VITE_APP_FRAME` 或挂载节点。
- 把 `VITE_APP_SERVER_URL` 写成带后端服务名的业务接口前缀；它应是后端网关服务地址。
- 未执行 dry-run 就正式写入。
- 缺少 `.npmrc` 就安装依赖。
- 把 `auto-imports.d.ts`、`components.d.ts`、`router-map.d.ts` 当作模板文件复制。
- 生成后改写 `vite.config.ts` 为手写 router。
- 忘记同步 `index.html`、`src/main.ts`、`src/styles/index.scss` 的挂载节点。
- typecheck 失败时直接改业务代码，而不是先确认自动生成声明文件是否缺失。
