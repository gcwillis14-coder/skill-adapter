# Installation & Cross-Agent Setup

`skill-adapter` follows the open [agentskills.io](https://agentskills.io) directory specification (`SKILL.md` + `references/`). No MCP server, background daemon, or build step is required—installation is a directory copy or symlink.

Keep `skill-adapter` installed at the **user (global) level** so you can invoke it inside any repository, while installing the **adapted skills it generates** into each target repository's **project-local** skills directory.

## Why Standalone Skill Packaging (Instead of a Plugin)?

`skill-adapter` ships as a standalone skill directory (`skills/skill-adapter/`) rather than a native plugin bundle (`plugin.json`):

- **Single self-contained capability:** Native plugins are designed to bundle multiple components—skills, subagents, always-on rules (`rules/AGENTS.md`), lifecycle hooks (`hooks.json`), and MCP server configs (`mcp_config.json`)—into a single toggleable unit under a global plugin namespace. `skill-adapter` has no MCP servers, no hooks, no subagents, and no always-on rules.
- **Cross-client portability:** A plain `skills/skill-adapter/` directory works identically across Claude Code, OpenAI Codex CLI, and Google Antigravity (`agy` CLI, Antigravity IDE, and Antigravity 2.0) without manifest conversion, plugin registration, or namespace collisions.
- **Zero idle overhead:** No plugin manifest or background services are loaded when you are not adapting a skill.

## Discovery Locations by Client

| Client | User-Level Path (Recommended for `skill-adapter`) | Project-Local Path (Recommended for Adapted Output) | Invocation |
| :--- | :--- | :--- | :--- |
| **Claude Code** (CLI & IDE extension) | `~/.claude/skills/skill-adapter/` | `<repo>/.claude/skills/<name>/` | `/skill-adapter` |
| **OpenAI Codex CLI** | `~/.agents/skills/skill-adapter/` | `<repo>/.agents/skills/<name>/` | `$skill-adapter` |
| **Google Antigravity** (`agy` CLI, Antigravity IDE, Antigravity 2.0) | `~/.gemini/config/skills/skill-adapter/` | `<repo>/.agents/skills/<name>/` | Explicit prompt or client skill trigger (see below) |

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

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd skill-adapter
```

### 2. Install for Your Active Client(s)

> [!NOTE]
> **Symlinks vs. `cp -r` (Windows & Sandbox Caveat):**
> Symlinking (`ln -s`) lets you update via `git pull`, but on **Windows** symlinks require Developer Mode or elevated privileges, and inside **sandboxed or containerized agents** symlinks pointing outside the workspace root may not be readable. In those environments, copy the directory with `cp -r` instead.

#### Option A: Claude Code

```bash
mkdir -p ~/.claude/skills
cp -r skills/skill-adapter ~/.claude/skills/skill-adapter
# Or symlink (POSIX, non-sandboxed):
# ln -s "$(pwd)/skills/skill-adapter" ~/.claude/skills/skill-adapter
```

#### Option B: OpenAI Codex CLI (and `.agents/skills` Compatible Tools)

```bash
mkdir -p ~/.agents/skills
cp -r skills/skill-adapter ~/.agents/skills/skill-adapter
# Or symlink (POSIX, non-sandboxed):
# ln -s "$(pwd)/skills/skill-adapter" ~/.agents/skills/skill-adapter
```

#### Option C: Google Antigravity (`agy` CLI, Antigravity IDE, Antigravity 2.0)

Global installation (available across all workspaces):

```bash
mkdir -p ~/.gemini/config/skills
cp -r skills/skill-adapter ~/.gemini/config/skills/skill-adapter
```

Or workspace-scoped installation (inside a specific repository):

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

## Tested Compatibility

The v1 verification suite ([tests/results.md](../tests/results.md)) verified the following in an **offline, sandboxed Python 3.15 environment** against `skills/skill-adapter/SKILL.md` (116 lines) and its bundled `references/`:

- **Structural validation (`python3 tests/validate_skills.py`):** 10/10 passed across `skills/skill-adapter/` and all 9 fixture skills, and 5/5 generated adapted skills passed (`EVAL-01`, `02`, `05`, `06`, `07`).
- **Validator unit tests (`python3 -m unittest discover -s tests -v`):** 7/7 tests passed.
- **Behavioral evaluations (`EVAL-01`–`EVAL-07`):** 7/7 passed across No Skill vs. Unadapted Original vs. Adapted Skill comparisons, covering Gate 1 security rejection (`EVAL-04`), Gate 2 unadaptable hard stop (`EVAL-03`), degradable manual fallbacks (`EVAL-01`, `02`, `06`, `07`), multi-file `scripts/` + `references/` + `.agents/skills/` collision scoping (`EVAL-06`), and v2 `metadata:` re-adaptation (`EVAL-07`).
- **Scope note:** Evaluations ran against synthetic fixture repositories (`tests/fixtures/`) without live external CLI installations of Claude Code, OpenAI Codex CLI, or Google Antigravity, without `node_modules/`, and without outbound network access. Client discovery paths above follow documented client conventions and were not tested in live external client binaries during this run.

See [README.md](../README.md) for an overview and [skills/skill-adapter/SKILL.md](../skills/skill-adapter/SKILL.md) for the skill definition.
