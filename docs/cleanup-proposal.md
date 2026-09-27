# 旧版清理记录（已执行）

用户于 2026-09-27 明确批准下列清单，现已执行。新版本由 team/ 提升至仓库根目录，旧平台适配和被替代内容已删除。下列路径保留迁移前表述，用于核对清理范围。

基线：8ca22dba9a94f28898bbce59f2537ff4d87c747d。所有路径相对于仓库根目录。执行前已核对新增、忽略及未提交文件，并验证所有删除路径位于仓库根目录内；保留了 .git、LICENSE、CODE_OF_CONDUCT.md、版权声明及全部新版本文件。

## 1. 删除原平台接入

目录：.agents/plugins/、.claude-plugin/、.codex-plugin/、.cursor-plugin/、.devin-plugin/、.hermes-plugin/、.kimi-plugin/、.muse-plugin/、.opencode/、.pi/、hooks/。

文件：GEMINI.md、gemini-extension.json、index.js、package.json、.version-bump.json、.pre-commit-config.yaml。

效果：原插件安装与自动 bootstrap 入口停止可用；仅使用新的团队指令和技能包。

## 2. 用新版本替换旧技能与辅助内容

- 原 skills/：由 team/skills/ 中 9 个技能替代，逐项职责迁移见 migration.md。
- 原 scripts/：由新打包/验证工具替代，旧版发布和平台同步工具退出。
- 原 tests/：平台和旧实现测试退出；新团队打包测试和行为评测保留。
- 原 docs/：平台安装、旧实现方案及历史设计文档退出；新协作协议、示例、迁移记录和配置指南保留。
- 原 assets/：两个旧插件展示资源退出；新版本无引用。
- RELEASE-NOTES.md：旧版发布记录退出，新版本保留基线来源说明。
- 原 .github/ISSUE_TEMPLATE/、FUNDING.yml、PULL_REQUEST_TEMPLATE.md：上游支持/捐赠/投稿模板退出；保留新团队 CI。

## 3. 最终布局

把 team/ 中的新 agents/、skills/、scripts/、tests/、docs/、evals/、team.json、README.md、AGENTS.md 和文本配置提升到仓库根目录，调整 CI 的工作目录，移除重复 team/ 容器目录。保留 LICENSE、CODE_OF_CONDUCT.md 和全部 Git 历史。重跑校验、单元测试、打包与 diff 检查。

本次仅完成本地清理和迁移，没有推送、创建上游 PR 或部署 Multica。
