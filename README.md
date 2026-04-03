# 🌌 Antigravity: Core Agentic Skills

![Antigravity Banner](https://img.shields.io/badge/Antigravity-Core%20Skills-purple?style=for-the-badge&logo=probot)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Category](https://img.shields.io/badge/AI-Agentic%20Orchestration-orange?style=flat-square)

> **Transform your AI assistant from a simple chatbot into a disciplined Senior Software Engineer.**

**Antigravity Core Skills** is a collection of modular, professional-grade workflows and safety protocols designed for the Antigravity AI framework. These skills port the rigorous engineering discipline found in top-tier agents—such as **Claude Code**—into universal, portable markdown-based skill sets.

---

## 📦 Professional Skills Library

Each skill is a standalone directory containing a `SKILL.md` file that defines its behavior, logic, and safety guardrails.

| Skill | Description | Workflow |
| :--- | :--- | :--- |
| **[🏗️ Agent Orchestrator](./agent_orchestrator/SKILL.md)** | Professional task decomposition. Spawns workers, synthesizes research, and manages the implementation lifecycle. | `orchestration` |
| **[🛡️ Permission Guard](./permission_guard/SKILL.md)** | Safety-first protocol for destructive operations. Implements explicit consent and confirmation workflows. | `security` |
| **[🔱 Git Workflow Master](./git_workflow_master/SKILL.md)** | Standardizes git management with safety protocols, secret scanning, and automated PR generation. | `version-control` |
| **[📝 File Editor Pro](./file_editor_pro/SKILL.md)** | Precise, non-destructive file editing with stale-read protection and isolation of target changes. | `file-ops` |
| **[⚖️ Code Review Expert](./code_review_expert/SKILL.md)** | Dual-phase code review (architecture + security) with vulnerability confidence scoring. | `quality-assurance` |

---

## ⚡ Why Use These Skills?

Current AI models are powerful, but often "loose" in their execution—they may skip tests, ignore security edge cases, or make sloppy file edits. **Antigravity Core** enforces a **Senior Engineering mindset**:

- **Stale-Read Protection**: Never edits a file without first confirming the current state.
- **Context Synthesis**: Orchestrators MUST synthesize findings before making changes, preventing "blind delegation."
- **Security First**: 3-phase security audits are baked into code reviews by default.
- **Workflow Isolation**: Tasks are broken into research, synthesis, and implementation phases to reduce hallucination.

---

## 🚀 Getting Started

### 1. Installation
Simply clone this repository or copy the desired skill folders into your Antigravity skills directory:

```bash
# Inside your project
cp -r /path/to/antigravity-core-skills/agent_orchestrator .agent/skills/
```

### 2. Global Use
For system-wide access, place them in your global configuration:
- **Windows**: `%USERPROFILE%\.gemini\antigravity\skills\`
- **Linux/macOS**: `~/.gemini/antigravity/skills/`

### 3. Usage
Once installed, you can invoke these skills by name within your conversation:
> "Run `@[code_review_expert]` on my last commit and focus on security."

---

## 💡 The "Claude Code" Paradigm Shift

This project was built from deep research into the routing, tool safety, and cognitive constraints seen in high-end agentic systems. We extracted the *architectural soul* of professional coding agents and converted it into **Universal Prompt Engineering**.

Instead of complex backend code, we use **Strict Structural Markdown**. This allows the AI to follow complex logic (like state machines or multi-phase workflows) natively within its own reasoning chain, regardless of the underlying LLM provider.

---

## ⚖️ Disclaimer

*This project is an independent synthesis of engineering workflows. It **does not** contain any source code, proprietary algorithms, or copyrighted material from Anthropic or other AI providers. It is not affiliated with or endorsed by any third party.*

---
<p align="center">Built for the next generation of AI-Native Engineering.</p>
