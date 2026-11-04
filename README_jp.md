# AI Orchestration

## 概要

AI Orchestrationは、複数のリポジトリで作業する際のagentの役割、委譲、エスカレーション、ガバナンスの共通ルールを提供します。まず[agentの役割](agents/README.md)と[実行ポリシー](docs/ai/policies.md)を確認し、各runtimeでの読込み・適用方法を検証してください。本repoは作業の調整ルールを定め、タスク実行は実装しません。

| リポジトリ | 担当範囲 |
| --- | --- |
| `ai-orchestration` | ポリシー、アーキテクチャ、役割、委譲、エスカレーション、ガバナンス |
| `agent-orchestrator` | ランタイム実装、スケジューリング、実行、監視、タスクのライフサイクル |

## 導入・連携

パッケージのインストール手順はありません。ランタイム側のプロジェクトは、ポリシー本文を複製せず、この正本を参照します。ポリシーの読込みや適用については、ランタイム側で実装と動作を確認して記録してください。リンクだけでは適用された証拠になりません。

## 使い方

作業を割り当てるときは[agentの役割](agents/README.md)を、委譲やエスカレーションの判断前には[実行ポリシー](docs/ai/policies.md)を参照してください。ランタイム固有のコマンドや動作は `agent-orchestrator` で管理します。

## 発展的な使い方

- [技術文書ポリシー](docs/ai/documentation-policy_jp.md)と[英語正本](docs/ai/documentation-policy.md)
- [技術文書agent](.codex/agents/technical-documentation.toml)
- 再利用できる[文書構成skill](.agents/skills/documentation-architect/SKILL.md)、[技術ライターskill](.agents/skills/technical-writer/SKILL.md)、[README保守skill](.agents/skills/readme-maintainer/SKILL.md)、[レビューskill](.agents/skills/documentation-reviewer/SKILL.md)
- [ドキュメント棚卸しとREADME移行表](docs/ai/documentation-inventory.md)

## ドキュメント

- [オーケストレーションのアーキテクチャ](docs/ai/orchestration.md)
- [実行ポリシー](docs/ai/policies.md)
- [agentの役割](agents/README.md)と[skillの規約](skills/README.md)
- [ドキュメントサイトの試作](docs/index.md)
- [英語README](README.md)
