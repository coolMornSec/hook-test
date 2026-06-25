#!/usr/bin/env node

import {
  existsSync,
  mkdtempSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join, resolve, sep } from "node:path";
import { spawnSync } from "node:child_process";

const defaultTemplate =
  "https://dev.magustek.com/bigdata/magus-basic-platform/magus-ai/magus-init-skeleton.git";
const defaultRef = "dev";
const frameEnvName = "VITE_APP_FRAME";

const requiredFiles = [
  ".env",
  ".env.development",
  ".env.production",
  ".npmrc",
  "index.html",
  "package.json",
  "src/main.ts",
  "src/router/index.ts",
  "src/styles/index.scss",
  "tsconfig.json",
  "vite.config.ts",
];

const excludedDirectories = new Set([
  ".git",
  "node_modules",
  "dist",
  "dist-ssr",
  ".cache",
  ".turbo",
]);

const excludedFiles = new Set([
  ".eslintrc-auto-import.json",
  "auto-imports.d.ts",
  "components.d.ts",
  "router-map.d.ts",
]);

function parseArgs(argv) {
  const args = { dryRun: false, force: false };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];

    if (arg === "--force") {
      args.force = true;
      continue;
    }

    if (arg === "--dry-run") {
      args.dryRun = true;
      continue;
    }

    if (!arg.startsWith("--")) {
      throw new Error(`Unexpected argument: ${arg}`);
    }

    const key = arg.slice(2);
    const value = argv[index + 1];

    if (value === undefined || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }

    args[key] = value;
    index += 1;
  }

  return args;
}

function requireArgs(args) {
  const requiredArgs = [
    "target",
    "packageName",
    "base",
    "port",
    "serverUrl",
    "frame",
    "mountElementId",
  ];
  const missing = requiredArgs.filter((key) => !(key in args) || !args[key]);

  if (missing.length > 0) {
    throw new Error(`Missing required arguments: ${missing.join(", ")}`);
  }

  const frame = args.frame.toUpperCase();

  if (!["YES", "NO"].includes(frame)) {
    throw new Error("--frame must be YES or NO");
  }

  if (args.base && (/^\//.test(args.base) || /\/$/.test(args.base))) {
    throw new Error("--base must be the micro-frontend deployment prefix and must not start or end with '/'.");
  }

  if (!/^\d+$/.test(args.port)) {
    throw new Error("--port must be a numeric string");
  }

  return {
    ...args,
    frame,
    template: args.template || defaultTemplate,
    ref: args.ref || defaultRef,
  };
}

function isGitTemplate(template) {
  return (
    /^https?:\/\//.test(template) ||
    /^git@/.test(template) ||
    template.endsWith(".git")
  );
}

function runCommand(command, args, options = {}) {
  const result = spawnSync(command, args, {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    ...options,
  });

  if (result.status !== 0) {
    const output = [result.stdout, result.stderr].filter(Boolean).join("\n");
    throw new Error(
      [`Command failed: ${command} ${args.join(" ")}`, output.trim()]
        .filter(Boolean)
        .join("\n"),
    );
  }

  return result;
}

function resolveTemplate(args) {
  if (!isGitTemplate(args.template)) {
    const templateDir = resolve(args.template);

    if (!existsSync(templateDir) || !statSync(templateDir).isDirectory()) {
      throw new Error(`Template directory does not exist: ${templateDir}`);
    }

    return { templateDir, cleanup: () => {}, sourceLabel: templateDir };
  }

  const tempRoot = mkdtempSync(join(tmpdir(), "magus-init-skeleton-"));
  const templateDir = join(tempRoot, "template");

  try {
    try {
      runCommand("git", [
        "clone",
        "--depth",
        "1",
        "--branch",
        args.ref,
        args.template,
        templateDir,
      ]);
    } catch (error) {
      runCommand("git", ["clone", "--depth", "1", args.template, templateDir]);
      runCommand("git", ["checkout", args.ref], { cwd: templateDir });
    }
  } catch (error) {
    rmSync(tempRoot, { recursive: true, force: true });
    throw error;
  }

  return {
    templateDir,
    sourceLabel: `${args.template}#${args.ref}`,
    cleanup: () => rmSync(tempRoot, { recursive: true, force: true }),
  };
}

function toRelativePath(root, filePath) {
  return filePath.slice(root.length + 1).split(sep).join("/");
}

function collectTemplateFiles(templateDir, currentDir = templateDir) {
  const files = [];

  for (const entry of readdirSync(currentDir, { withFileTypes: true })) {
    const name = entry.name;
    const fullPath = join(currentDir, name);
    const relativePath = toRelativePath(templateDir, fullPath);

    if (entry.isDirectory()) {
      if (!excludedDirectories.has(name)) {
        files.push(...collectTemplateFiles(templateDir, fullPath));
      }
      continue;
    }

    if (entry.isFile() && !excludedFiles.has(basename(relativePath))) {
      files.push(relativePath);
    }
  }

  return files.sort();
}

function readTemplateFiles(templateDir) {
  const files = collectTemplateFiles(templateDir);
  const renderedFiles = new Map();

  for (const filePath of files) {
    renderedFiles.set(filePath, readFileSync(join(templateDir, filePath)));
  }

  return renderedFiles;
}

function isText(buffer) {
  return !buffer.includes(0);
}

function asText(renderedFiles, filePath) {
  const buffer = renderedFiles.get(filePath);

  if (!buffer) {
    return "";
  }

  return buffer.toString("utf8");
}

function setText(renderedFiles, filePath, content) {
  renderedFiles.set(filePath, Buffer.from(content, "utf8"));
}

function renderEnv(args, production = false) {
  return [
    `VITE_APP_BASE=${args.base}`,
    `VITE_APP_PORT=${args.port}`,
    `VITE_APP_SERVER_URL=${args.serverUrl}`,
    "",
    "# 默认采用微前端开发布局",
    `${frameEnvName}=${production ? "NO" : args.frame}`,
    "",
  ].join("\n");
}

function replaceAll(content, search, replacement, filePath) {
  if (!content.includes(search)) {
    throw new Error(`Template anchor not found in ${filePath}: ${search}`);
  }

  return content.split(search).join(replacement);
}

function renderProject(renderedFiles, args) {
  setText(renderedFiles, ".env", renderEnv(args));
  setText(renderedFiles, ".env.development", renderEnv(args));
  setText(renderedFiles, ".env.production", renderEnv(args, true));

  const packageJson = JSON.parse(asText(renderedFiles, "package.json"));
  packageJson.name = args.packageName;
  delete packageJson.scripts?.["template:generate"];
  setText(renderedFiles, "package.json", `${JSON.stringify(packageJson, null, 2)}\n`);

  let indexHtml = asText(renderedFiles, "index.html");
  indexHtml = indexHtml.replace(
    /<title>[\s\S]*?<\/title>/,
    `<title>${args.packageName}</title>`,
  );
  indexHtml = indexHtml.replace(
    /<div id="[^"]+"><\/div>/,
    `<div id="${args.mountElementId}"></div>`,
  );
  setText(renderedFiles, "index.html", indexHtml);

  const mountReplacement = `#${args.mountElementId}`;
  setText(
    renderedFiles,
    "src/main.ts",
    replaceAll(
      asText(renderedFiles, "src/main.ts"),
      "#magus-init",
      mountReplacement,
      "src/main.ts",
    ),
  );
  setText(
    renderedFiles,
    "src/styles/index.scss",
    replaceAll(
      asText(renderedFiles, "src/styles/index.scss"),
      "#magus-init",
      mountReplacement,
      "src/styles/index.scss",
    ),
  );

  let viteConfig = asText(renderedFiles, "vite.config.ts");
  viteConfig = viteConfig.replace(
    /path:\s*appBase\s*\?\s*`\$\{appBase\}\/`\s*:\s*["']{2}/g,
    "path: ''",
  );
  viteConfig = viteConfig.replace(
    /open:\s*`\/\$\{appBase\}\/\$\{appBase\}`/g,
    "open: appBase ? `/${appBase}/` : '/'",
  );
  setText(renderedFiles, "vite.config.ts", viteConfig);

  const routerIndex = asText(renderedFiles, "src/router/index.ts")
    .replaceAll("createWebHistory(base)", "createWebHistory(import.meta.env.BASE_URL)")
    .replaceAll(
      "createWebHistory(import.meta.env.VITE_APP_BASE)",
      "createWebHistory(import.meta.env.BASE_URL)",
    );
  setText(renderedFiles, "src/router/index.ts", routerIndex);

  return renderedFiles;
}

function assertRequiredFiles(renderedFiles) {
  const missing = requiredFiles.filter((filePath) => !renderedFiles.has(filePath));

  if (missing.length > 0) {
    throw new Error(
      [
        "Template project is missing required files:",
        ...missing.map((filePath) => `- ${filePath}`),
      ].join("\n"),
    );
  }
}

function assertNoExistingFiles(target, renderedFiles, force) {
  if (force) {
    return;
  }

  const existing = [...renderedFiles.keys()].filter((filePath) =>
    existsSync(join(target, filePath)),
  );

  if (existing.length > 0) {
    throw new Error(
      [
        "Target already contains files. Re-run with --force only after user approval:",
        ...existing.map((filePath) => `- ${filePath}`),
      ].join("\n"),
    );
  }
}

function validateRenderedFiles(renderedFiles, args) {
  assertRequiredFiles(renderedFiles);

  for (const [filePath, content] of renderedFiles.entries()) {
    if (isText(content) && /\{\{[A-Z0-9_]+\}\}/.test(content.toString("utf8"))) {
      throw new Error(`Rendered skeleton still contains unresolved placeholders: ${filePath}`);
    }
  }

  const npmrc = asText(renderedFiles, ".npmrc");

  if (!npmrc.includes("@magustek:registry")) {
    throw new Error(".npmrc is missing @magustek:registry");
  }

  const packageJson = JSON.parse(asText(renderedFiles, "package.json"));

  if (packageJson.name !== args.packageName) {
    throw new Error(
      `package.json name mismatch: expected ${args.packageName}, got ${packageJson.name}`,
    );
  }

  const indexHtml = asText(renderedFiles, "index.html");

  if (!indexHtml.includes(`<title>${args.packageName}</title>`)) {
    throw new Error("index.html title does not match packageName");
  }

  if (!indexHtml.includes(`id="${args.mountElementId}"`)) {
    throw new Error("index.html root id does not match mountElementId");
  }

  const mainTs = asText(renderedFiles, "src/main.ts");

  if (!mainTs.includes(`app.mount('#${args.mountElementId}')`)) {
    throw new Error("src/main.ts mount selector does not match mountElementId");
  }

  const styleIndex = asText(renderedFiles, "src/styles/index.scss");

  if (!styleIndex.includes(`#${args.mountElementId}`)) {
    throw new Error(
      "src/styles/index.scss root selector does not match mountElementId",
    );
  }

  const envChecks = [
    [".env", args.frame],
    [".env.development", args.frame],
    [".env.production", "NO"],
  ];

  for (const [filePath, layout] of envChecks) {
    const content = asText(renderedFiles, filePath);

    for (const expectedLine of [
      `VITE_APP_BASE=${args.base}`,
      `VITE_APP_PORT=${args.port}`,
      `VITE_APP_SERVER_URL=${args.serverUrl}`,
      `${frameEnvName}=${layout}`,
    ]) {
      if (!content.includes(expectedLine)) {
        throw new Error(`${filePath} is missing ${expectedLine}`);
      }
    }
  }

  const viteConfig = asText(renderedFiles, "vite.config.ts");
  const viteChecks = [
    ["vue-router/vite", "vite.config.ts must import VueRouter from vue-router/vite"],
    ["vue-router/unplugin", "vite.config.ts must import VueRouterAutoImports from vue-router/unplugin"],
    ["VueRouter(", "vite.config.ts must register VueRouter(...)"],
    ["src/pages", "vite.config.ts VueRouter file-based route config must include src/pages"],
    ["VueRouterAutoImports", "vite.config.ts AutoImport imports must include VueRouterAutoImports"],
    ["loadEnv(", "vite.config.ts must use loadEnv(...)"],
    ["VITE_APP_BASE", "vite.config.ts must read VITE_APP_BASE"],
    ["VITE_APP_PORT", "vite.config.ts must read VITE_APP_PORT"],
    ["VITE_APP_SERVER_URL", "vite.config.ts must read VITE_APP_SERVER_URL"],
  ];

  for (const [needle, message] of viteChecks) {
    if (!viteConfig.includes(needle)) {
      throw new Error(message);
    }
  }

  if (!/VueRouter\([\s\S]*src\/pages/.test(viteConfig)) {
    throw new Error(
      "vite.config.ts VueRouter file-based route config must include src/pages",
    );
  }

  if (/open:\s*`\/\$\{appBase\}\/\$\{appBase\}`/.test(viteConfig)) {
    throw new Error("vite.config.ts server.open must be derived from VITE_APP_BASE once");
  }

  const routerIndex = asText(renderedFiles, "src/router/index.ts");

  if (!routerIndex.includes("createWebHistory(import.meta.env.BASE_URL)")) {
    throw new Error(
      "src/router/index.ts must use createWebHistory(import.meta.env.BASE_URL)",
    );
  }
}

function writeRenderedFiles(target, renderedFiles) {
  mkdirSync(target, { recursive: true });

  for (const [filePath, content] of renderedFiles.entries()) {
    const outputPath = join(target, filePath);

    mkdirSync(dirname(outputPath), { recursive: true });
    writeFileSync(outputPath, content);
  }
}

function run() {
  const args = requireArgs(parseArgs(process.argv.slice(2)));
  const target = resolve(args.target);
  const template = resolveTemplate(args);

  try {
    const renderedFiles = renderProject(readTemplateFiles(template.templateDir), args);

    validateRenderedFiles(renderedFiles, args);

    if (args.dryRun) {
      console.log("Dry run passed. No files were written.");
      console.log(`Template source: ${template.sourceLabel}`);
      console.log(`Files checked: ${renderedFiles.size}`);
      return;
    }

    assertNoExistingFiles(target, renderedFiles, args.force);
    writeRenderedFiles(target, renderedFiles);
    validateRenderedFiles(renderedFiles, args);

    console.log(`Generated Magus frontend skeleton at ${target}`);
    console.log(`Template source: ${template.sourceLabel}`);
    console.log(`Files written: ${renderedFiles.size}`);
  } finally {
    template.cleanup();
  }
}

try {
  run();
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
