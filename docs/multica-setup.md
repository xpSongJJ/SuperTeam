# Multica 配置

本仓库提供通用角色和 skills；以下是配置步骤，不包含平台运行时适配代码。未在你的 Multica 实例上执行创建、导入或联调。

1. 在仓库根目录运行 `python scripts/team.py check` 和 `python scripts/team.py build --out dist/team-v1`。
2. 创建三个独立 Agent：Planner、Frontend Lead、Backend Lead。Planner 配置你选择的更强模型；两端 Lead 配置适合执行明确任务的模型。仓库不硬编码模型名称，也不保证运行时具备动态切换模型能力。
3. 分别将导出的完整 `instructions.md` 填入角色 instructions，不能只放入展示用 description。
4. 导入每个 skill 目录及其模板。给 Planner 绑定 7 个 skills，前后端各 5 个。四个 shared skills 可在工作区只导入一次，再同时绑定三个 Agent；不要重复创建同名技能。确认导入内容包含模板和版本。
5. 建立团队/Squad，以 Planner 为 leader，加入前后端 Lead。团队路由规则可以写在 Squad instructions；所有成员必须遵守的规则已经写入各角色 instructions，不能只依赖 leader 收到的配置。
6. 指定一个共同任务存储和代码仓库。不同机器上的本地路径不能直接当成共享交接路径；使用可访问的仓库记录或任务附件，明确版本。安排独立工作区和共享文件所有权。
7. 检查运行时能否创建独立上下文子 Agent、保留报告、配置并发及运行测试。默认一层子 Agent；不支持时执行者可以串行工作，独立评审需要另一个真实 Agent。没有独立评审时保持待评审，不能假装成功。
8. 验证共享并发预算：四个全局子 Agent 槽位、每角色至多两个。没有原子槽位记录能力时，由 Planner 串行发放调度许可。配置 runtime 的实际限制；文本规则本身不是并发锁。
9. 用 [交付示例](worked-example.md) 跑一次真实小功能，再开启大任务。确认三个角色都能读取自己的指令、skills、模板和共同任务记录。

## 首次验证应留下的证据

- 三个 Agent 配置和绑定的技能版本；无需记录密钥。
- Planner 的任务包/契约记录与实际 Lead 接收结果。
- 实现者和独立评审者身份、工作区隔离、子 Agent 结束后的报告。
- 前后端候选版本、Planner 集成版本、真实端到端检查。
- 中断一次后能从持久化记录继续，且不重复派发已完成任务。

配置成功不等于子 Agent 已正常运行；模拟场景通过也不等于业务功能通过。

参考官方文档：[Agents](https://multica.ai/docs/agents)、[Skills](https://multica.ai/docs/skills)、[Squads](https://multica.ai/docs/squads)。平台界面变化时以实际界面和官方文档为准。
