# 技能行为验证

这里保留三角色工作流的可复现场景和记录。运行工具仅使用 Python 标准库；模型评测额外要求本机已经安装、登录 Codex CLI。它是维护时可选工具，不是使用 skills 的依赖。

## 本地确定性检查

```text
python scripts/team.py check
python -m unittest discover -s tests -v
python scripts/team.py build --out dist/check-1
```

这些检查验证绑定、名称、引用可移植性和真实打包行为，不证明模型会遵守规则。

打包器支持简单 inline/reference Markdown 链接、可选引号标题和代码块/行内代码排除；本地资源必须使用相对路径，复杂文件名用 URL 编码。它不是完整 CommonMark 解析器。常驻 instructions 必须自包含，资源放入 skill。它拒绝覆盖已有导出，先在临时目录构建再发布完整目录。

## 模型场景

```text
python scripts/run_evals.py baseline --out evals/local-runs/before --samples 5
python scripts/run_evals.py guided --out evals/local-runs/after --samples 5
python scripts/run_evals.py guided --out evals/local-runs/planner-fix --samples 5 --cases P1
```

使用新的输出目录保留历次记录。脚本为每个样本建立独立临时工作区、只读 ephemeral CLI 会话，最多并发两个，默认每次 240 秒超时。使用当前 CLI 配置中的模型，不自动修改账号或模型设置。输入是 scenarios.txt 和 guided 模式下的角色/skill 文本；运行前检查这些文件不含业务秘密。会产生正常模型用量。

先保存无新规则基线，再给出规则。每个样本含相同压力场景。读取原始回答，不用关键词计数代替语义判定。还应记录模型、CLI、已加载全局配置及限制。此脚本把三个角色规则一起提供给一个模型进行决策模拟，不能证明三个 Agent 实际协作、调度隔离或 Multica 自动触发。

| 场景 | 观察对象 |
|---|---|
| P1 | 区分已授权实施与尚未决定的产品语义，生成有依赖的任务交接 |
| P2 | Planner 接手困难算法/关键实现，避免反复派回执行角色 |
| C1 | 不让已有实现或期限悄悄改变契约 |
| D1 | 一层子 Agent、全局预算、隔离写入、共享文件所有权 |
| F1 | mock、键盘缺陷和未测会话行为不能冒充完成 |
| B1 | 并发副作用、租户授权和数据恢复的领域门槛 |
| R1 | Planner 也不能自审；旧提交评审不能覆盖新提交 |
| I1 | Planner 对组合版本、真实联调和最终验收负责 |
| V1 | 恢复真实版本与证据，明确跳过/未运行，不捏造结果 |

工程包的独立审查只审查本轮新写的通用工具和合成测试。完整角色包外发审查被自动审批拒绝后缩小了范围；没有通过其他渠道发送原仓库内容。最终局限见 results.md。
