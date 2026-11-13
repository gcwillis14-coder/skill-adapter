# Installation & Cross-Agent Setup

`skill-adapter` follows the open [agentskills.io](https://agentskills.io) directory specification (`SKILL.md` + `references/` + `scripts/`). No MCP server, background daemon, or build step is required—installation is a directory copy or symlink.

Keep `skill-adapter` installed at the **user (global) level** so you can invoke it inside any repository, while installing the **adapted skills it generates** into each target repository's **project-local** skills directory.

## Why Standalone Skill Packaging (Instead of a Plugin)?

`skill-adapter` ships as a standalone skill directory (`skills/skill-adapter/`) rather than a native plugin bundle (`plugin.json`):

- **Single self-contained capability:** Native plugins are designed to bundle multiple components—skills, subagents, always-on rules (`rules/AGENTS.md`), lifecycle hooks (`hooks.json`), and MCP server configs (`mcp_config.json`)—into a single toggleable unit under a global plugin namespace. `skill-adapter` has no MCP servers, no hooks, no subagents, and no always-on rules.
- **Cross-client portability:** A plain `skills/skill-adapter/` directory works identically across Claude Code, OpenAI Codex CLI, and Google Antigravity (`agy` CLI, Antigravity IDE, and Antigravity 2.0) without manifest conversion, plugin registration, or namespace collisions.
- **Zero idle overhead:** No plugin manifest or background services are loaded when you are not adapting a skill.

## Discovery Locations by Client

Most modern coding agents and IDEs follow the open `agentskills.io` layout (`SKILL.md` + `references/` + `scripts/`), either via the shared `.agents/skills/` path or a client-specific folder:

| Client / IDE | User-Level Path (for `skill-adapter`) | Project-Local Path (for Adapted Output) | Invocation |
| :--- | :--- | :--- | :--- |
| **Claude Code** (CLI & IDE) | `~/.claude/skills/skill-adapter/` | `<repo>/.claude/skills/<name>/` | `/skill-adapter` |
| **OpenAI Codex CLI** | `~/.agents/skills/skill-adapter/` | `<repo>/.agents/skills/<name>/` | `$skill-adapter` |
| **Google Antigravity** (`agy`, IDE, 2.0) | `~/.gemini/config/skills/skill-adapter/` | `<repo>/.agents/skills/<name>/` | Explicit prompt |
| **Cursor** | `~/.cursor/skills/skill-adapter/` (or `~/.agents/skills/`) | `<repo>/.cursor/skills/<name>/` (or `.agents/skills/`) | `/skill-adapter` or prompt |
| **Windsurf** | `~/.codeium/windsurf/skills/skill-adapter/` | `<repo>/.windsurf/skills/<name>/` | Explicit prompt |
| **GitHub Copilot** (VS Code) | `~/.copilot/skills/skill-adapter/` | `<repo>/.github/skills/<name>/` (or `.agents/skills/`) | `/skill-adapter` or prompt |
| **OpenCode / Gemini CLI / Other `agentskills.io` tools** | `~/.agents/skills/skill-adapter/` | `<repo>/.agents/skills/<name>/` | Client trigger or prompt |

### Google Antigravity Notes (`agy` CLI, Antigravity IDE, Antigravity 2.0)

- **Workspace discovery & precedence:** Antigravity scans `<repo>/.agents/skills/` (as well as `.agent/`, `_agents/`, and `_agent/`) walking up from the current working directory to the repository root. Workspace-scoped customizations take priority over global customizations in `~/.gemini/config/skills/`.
- **Skills vs. Rules (`GEMINI.md` / `AGENTS.md`):** Skills under `skills/<name>/SKILL.md` use progressive disclosure and load on demand. Directory-based rules in `GEMINI.md`, `AGENTS.md`, and `.agents/rules/*.md` are always active for their directory scope. When an external skill includes standing project conventions that belong in `GEMINI.md` or `AGENTS.md`, `skill-adapter` recommends those edits for your review instead of silently modifying rule files.

## Explicit Invocation (`disable-model-invocation: true`)

`skill-adapter` declares `disable-model-invocation: true` in its YAML frontmatter:

- **Zero idle context load:** Adapting an external skill is an intentional workflow, not an ambient coding rule. Disabling automatic model invocation keeps `skill-adapter` out of unrelated turns and avoids accidental auto-triggering.
- **Explicit trigger:** Invoke it directly with `/skill-adapter` in Claude Code or `$skill-adapter` in Codex CLI.
- **Fallback for clients without slash commands:** If your client or chat interface does not expose a slash command for `disable-model-invocation: true` skills, invoke it explicitly in your prompt by name or file path—for example:

  ```text
  Read ~/.gemini/config/skills/skill-adapter/SKILL.md and use it to adapt /path/to/external-skill for this repository.
  ```

## Ways to Install

### Option 1: Via `npx skills` (`skills.sh` / `agentskills.io` CLI)

If you use the `skills` CLI, install `skill-adapter` directly from GitHub into your chosen agents:

```bash
npx skills add https://github.com/gcwillis14-coder/skill-adapter
```

### Option 2: Clone & Copy or Symlink

#### 1. Clone the Repository

```bash
git clone https://github.com/gcwillis14-coder/skill-adapter.git
cd skill-adapter
```

#### 2. Copy (or Symlink) into Your Agent's Skills Directory

> [!NOTE]
> **Symlinks vs. `cp -r` (Windows & Sandbox Caveat):**
> Symlinking (`ln -s`) lets you update via `git pull`, but on **Windows** symlinks require Developer Mode or elevated privileges, and inside **sandboxed or containerized agents** symlinks pointing outside the workspace root may not be readable. In those environments, copy the directory with `cp -r` instead.

```bash
# Claude Code
mkdir -p ~/.claude/skills && cp -r skills/skill-adapter ~/.claude/skills/skill-adapter

# OpenAI Codex CLI / OpenCode / shared .agents/skills clients
mkdir -p ~/.agents/skills && cp -r skills/skill-adapter ~/.agents/skills/skill-adapter

# Google Antigravity (global)
mkdir -p ~/.gemini/config/skills && cp -r skills/skill-adapter ~/.gemini/config/skills/skill-adapter

# Cursor
mkdir -p ~/.cursor/skills && cp -r skills/skill-adapter ~/.cursor/skills/skill-adapter

# Windsurf
mkdir -p ~/.codeium/windsurf/skills && cp -r skills/skill-adapter ~/.codeium/windsurf/skills/skill-adapter

# GitHub Copilot (VS Code)
mkdir -p ~/.copilot/skills && cp -r skills/skill-adapter ~/.copilot/skills/skill-adapter
```

On POSIX systems without sandbox restrictions, you can replace `cp -r skills/skill-adapter ...` with `ln -s "$(pwd)/skills/skill-adapter" ...`.

#### Option 3: Workspace-Local Install (Single Repository)

If you prefer not to install globally, copy `skills/skill-adapter` into a single repository's `.agents/skills/` (or `.claude/skills/`, `.cursor/skills/`, `.windsurf/skills/`, `.github/skills/`):

```bash
mkdir -p <repo>/.agents/skills
cp -r skills/skill-adapter <repo>/.agents/skills/skill-adapter
```

## Lifecycle: Updating, Re-Adapting, and Removing

### Updating `skill-adapter`

- If installed via `ln -s`, run `git pull` in your clone.
- If installed via `cp -r`, re-run `cp -r skills/skill-adapter <target-skills-dir>/` after pulling updates.

### Re-Adapting an Existing Project Skill

When your repository stack changes or the upstream source skill is updated:

1. Check the YAML frontmatter `metadata:` provenance fields (`adapted_from`, `source_ref`, `adapted_date`, `key_overrides`) at the top of your project's adapted `SKILL.md`.
2. Run `skill-adapter` against the updated source skill and point it at your existing adapted skill directory so its three-way reconciliation workflow ([readapt-guide.md](../skills/skill-adapter/references/readapt-guide.md)) merges upstream changes while preserving valid local overrides.

### Uninstalling

Remove the `skill-adapter` directory or symlink from your user skills folder:

```bash
rm -rf ~/.claude/skills/skill-adapter ~/.agents/skills/skill-adapter ~/.gemini/config/skills/skill-adapter
```

Project-local adapted skills already generated inside your repositories remain self-contained and continue working independently.

## Input Formats `skill-adapter` Accepts

When adapting an external skill, you can point `skill-adapter` at any of the common ways skills are distributed:

- **Local directory:** `/path/to/skill-dir` (or an existing `~/.claude/skills/<name>` / `.agents/skills/<name>` install)
- **GitHub repository or subdirectory URL:** `https://github.com/<owner>/<repo>` or `https://github.com/<owner>/<repo>/tree/main/skills/<name>`
- **Multi-skill / plugin bundle:** Repositories with `plugin.json`, `.claude-plugin/`, `hooks/`, or multiple `skills/*/SKILL.md` folders (`skill-adapter` enumerates the suite and asks or scopes which skill(s) to adapt)
- **Existing adapted skill (for updates):** Point at both the updated upstream source and your local adapted skill directory to run a three-way merge

See [README.md](../README.md) for worked examples and [skills/skill-adapter/SKILL.md](../skills/skill-adapter/SKILL.md) for the skill definition.
