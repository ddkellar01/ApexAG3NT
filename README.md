# AGENTS.md — ApexAgent Operational Directives

## Core Mission
ApexAgent is a multi-model, agentic developer harness designed for high-throughput software engineering, autonomous bug remediation, and safe shell/AST execution.

## Architectural Rules
1. Multi-Stage Pipeline Execution:
   - Tier 1: Multimodal Ingestion & Context Caching (Gemini 2.5/3.0 Context Engine)
   - Tier 2: Deliberative Reasoning & Thinking Tokens (Gemini Thinking Engine)
   - Tier 3: DAG Decomposition & Multi-Model Dispatcher (Grok-style Router)
   - Tier 4: Execution Harness & REPL (Claude Code CLI + Codex AST Sandbox)
   - Tier 5: Dual-Loop Self-Healing & Verification (pytest / AST / Git rollback)

2. State & Safety Boundaries:
   - Always initialize a reversible Git snapshot before executing multi-file edits.
   - All code generation must be pre-validated in an isolated container/REPL sandbox.
   - Attach `thought_signatures` across multi-turn sub-agent interactions to preserve reasoning continuity.

3. System Hooks & Lifecycle:
   - Pre-edit: Verify target file locks and run AST parser.
   - Post-edit: Execute inner verification loop (unit tests + linter).
   - Fail-state: Trigger automatic snapshot rollback and pass stack trace back to Tier 2 Planner with original reasoning signature.
