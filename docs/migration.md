# 从 Superpowers 到三角色团队

来源：obra/superpowers，改造基线提交 `8ca22dba9a94f28898bbce59f2537ff4d87c747d`（工作区原始内容，版本 6.4.2）。保留 Git 历史及原 LICENSE，不向上游提交此团队定制改造。

## 职责迁移

| 原 skill | 新归属与变化 |
|---|---|
| using-superpowers | 每角色常驻 instructions + team.json 绑定，移除平台工具映射 |
| brainstorming | planning-delivery 负责产品目标；frontend-delivery 承接交互/视觉；solving-hard-problems 承接技术探索 |
| writing-plans | planning-delivery 写跨端任务包；两端交付 skills 细化本域实现和测试 |
| subagent-driven-development | delegating-work 的短期 worker + independent-review；困难实现允许由 Planner 亲自负责 |
| executing-plans | 各角色可直接执行小任务，保留独立评审和证据要求 |
| dispatching-parallel-agents | delegating-work，增加全局预算、共享文件所有权和禁止孙 Agent |
| using-git-worktrees | 常驻规则及 delegating-work 的隔离要求；移除平台原生工具适配 |
| test-driven-development | engineering-evidence 保留测试先行、正确失败原因、独立期望值和真实行为验证 |
| systematic-debugging | engineering-evidence 的复现/根因/假设验证，困难跨域问题交 Planner |
| verification-before-completion | engineering-evidence 的版本化证据 + Planner 的集成验收 |
| requesting-code-review / receiving-code-review | independent-review 的请求、双维度判定、证据核实、修复和重审 |
| finishing-a-development-branch | integrating-delivery，由 Planner 对跨角色组合版本负责 |
| diagnosing-superpowers | 任务/评审/验证记录保留诊断基础；不保留各平台会话解析、上游 issue 导出工具 |
| writing-skills | 维护流程移入 AGENTS.md 和 evals/，不绑定给三个业务角色 |

## 有意调整的行为

- 保留测试先行、根因调查、精确任务交接、独立评审和证据优先。
- 已确认的用户目标与实施授权不重复索取；不确定的技术路线由 Planner 决定，显式需求变化仍由人类决定。
- 原单控制器工作流中的决策、领域实现与最终集成拆到三个角色。
- 采用两轮失败后升级的初始预算；Planner 可记录新预算，不能据此绕过质量门槛。
- 修复历史/继承代码时记录真实基线，不为制造 TDD 历史而删除他人已有实现。
- 静态文档不写镜像断言；skills 以行为场景检验，打包代码以实际导出结果测试。
- 完成后保留任务/评审证据，不自动删除恢复记录。

这些是用户指定团队工作流的设计选择，不宣称比上游适合所有场景。实际评测结论和未覆盖内容见 evals/results.md。

## 已完成的清理范围

经用户明确批准，已完成：移除原平台插件目录、marketplace manifests、bootstrap hooks、平台安装说明、平台工具引用、平台专属测试、旧 npm/Pi/OpenCode 入口和版本同步脚本。移除不再被使用的可视化服务及配套资源、历史平台设计文档和上游发布记录。新仓库保留通用 Markdown skills、标准库 Python 工具、测试和团队使用说明。

原始内容仍可通过基线提交读取，例如 `git show 8ca22dba9a94f28898bbce59f2537ff4d87c747d:skills/writing-skills/SKILL.md`。恢复时先查看差异，不覆盖当前未提交改动。
