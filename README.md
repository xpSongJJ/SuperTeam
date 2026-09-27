# SuperTeam

基于 Superpowers 改造的三角色协作技能库。Planner 负责创造性、高难度工作、技术路线和最终集成；Frontend Lead / Backend Lead 负责确定范围内的实现、测试和评审交付。

这是面向自用团队的派生版本，已移除原项目的多平台适配及被替代内容，直接在仓库根目录提供角色指令、9 个 skills、交接模板和零第三方依赖的导出/检查工具；不会自动创建 Multica Agent，也不是调度服务。

## 三个角色

| 角色 | 负责 | 技能组合 |
|---|---|---|
| Planner | 需求、架构、困难问题与关键实现、调度、跨端集成、最终验收 | 3 个专属 + 4 个共享 |
| Frontend Lead | 交互与视觉设计、前端实现/测试、前端评审交付 | 1 个专属 + 4 个共享 |
| Backend Lead | 服务与数据实现、后端测试、迁移准备、后端评审交付 | 1 个专属 + 4 个共享 |

四个共享 skills：契约协作、子 Agent 委派、工程验证与恢复、独立评审。它们在源码中只维护一份，在导出时分别打包到三个角色中。

## 开始使用

在仓库根目录执行下列命令。Python 3.10+ 仅用于本地检查和导出，Agent 使用 Markdown skills 无需 Python 依赖。

```text
python scripts/team.py check
python -m unittest discover -s tests -v
python scripts/team.py build --out dist/team-v1
```

输出：

```text
dist/team-v1/
  planner/instructions.md
  planner/skills/...
  planner/bundle.json
  frontend/instructions.md
  frontend/skills/...
  frontend/bundle.json
  backend/instructions.md
  backend/skills/...
  backend/bundle.json
```

将各角色的完整 `instructions.md` 放入 Agent instructions，将其 `skills/` 下每个 skill 目录分别导入并绑定。每个 skill 的模板均放在目录内部；不要只复制 SKILL.md。已有输出目录不会被覆盖，更新时使用新目录名。`bundle.json` 是本地技能清单与内容校验信息，不是 Multica 原生导入配置。

配置源是 [team.json](team.json)，共享规则在 [agents/common.md](agents/common.md)。仅复制单独角色文件会遗漏公共规则，应使用导出的完整 instructions。

参阅 [Multica 配置步骤](docs/multica-setup.md)、[协作协议](docs/team-protocol.md)、[完整交付示例](docs/worked-example.md)、[原技能迁移表](docs/migration.md)和[验证说明](evals/README.md)。

## 核心约定

- Planner 对整个功能负责，可亲自实现困难代码。Lead 对各自领域交付负责。
- Contract 驱动；共享语义和接口变更由 Planner 协调，两端确认影响。
- Author 不等于 Reviewer，Planner 也不能自审签收自己的代码。
- 一级角色长期负责，子 Agent 短生命周期，默认禁止孙 Agent。
- 默认全功能最多 4 个活跃子 Agent、每角色最多 2 个；2 轮失败后升级。Planner 分配预算，运行时还需配置对应并发限制。
- Lead 交付 READY_FOR_INTEGRATION；Planner 在真实联调、业务验收和独立评审通过后设置 ACCEPTED。
- 任务记录保存版本、证据、阻塞和下一步；不会依赖永久聊天记忆。

当前验证范围与限制见 [评测报告](evals/results.md)。文本场景测试不等同于 Multica 端到端集成验证。

保留原项目 [MIT 许可证](LICENSE)与版权声明；来源及行为变化见迁移表。
