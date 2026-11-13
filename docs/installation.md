# Installation & Cross-Agent Setup

`skill-adapter` follows the open [agentskills.io](https://agentskills.io) directory specification (`SKILL.md` + `references/` + `scripts/`). No MCP server, background daemon, or build step is required—installation is a simple directory copy or symlink.

Keep `skill-adapter` installed at the **user (global) level** so you can invoke it inside any repository, while installing the **adapted skills it generates** into each target repository's **project-local** skills directory.

## Standalone Skill Packaging

`skill-adapter` ships as a standalone skill directory (`skills/skill-adapter/`) rather than a native plugin bundle:

- **Self-contained capability:** No MCP servers, background daemons, or lifecycle hooks.
- **Cross-client compatibility:** Adheres to standard `agentskills.io` directory conventions.
- **Zero idle overhead:** Nothing is loaded into context until you actively invoke the skill.

---

## Client Compatibility & Paths

### Tested & Verified Clients

These clients have been tested and verified directly with `skill-adapter`:

| Client / IDE | User-Level Path (for `skill-adapter`) | Project-Local Path (for Adapted Output) | Invocation |
| :--- | :--- | :--- | :--- |
| **OpenAI Codex CLI** | `~/.agents/skills/skill-adapter/` | `<repo>/.agents/skills/<name>/` | `$skill-adapter` or prompt |
| **Google Antigravity** (`agy`, IDE, 2.0) | `~/.gemini/config/skills/skill-adapter/` | `<repo>/.agents/skills/<name>/` | Explicit prompt |

### Untested Community Targets

Because `skill-adapter` follows standard `agentskills.io` conventions, these clients should work out of the box, but are currently untested by the maintainer. If you encounter any friction, please [open an issue](https://github.com/gcwillis14-coder/skill-adapter/issues).

| Client / IDE | User-Level Path (for `skill-adapter`) | Project-Local Path (for Adapted Output) | Invocation |
| :--- | :--- | :--- | :--- |
| **Claude Code** | `~/.claude/skills/skill-adapter/` | `<repo>/.claude/skills/<name>/` | `/skill-adapter` |
| **Cursor** | `~/.cursor/skills/skill-adapter/` (or `~/.agents/skills/`) | `<repo>/.cursor/skills/<name>/` (or `.agents/skills/`) | `/skill-adapter` or prompt |
| **Windsurf** | `~/.codeium/windsurf/skills/skill-adapter/` | `<repo>/.windsurf/skills/<name>/` | Explicit prompt |
| **GitHub Copilot** (VS Code) | `~/.copilot/skills/skill-adapter/` | `<repo>/.github/skills/<name>/` (or `.agents/skills/`) | `/skill-adapter` or prompt |
| **OpenCode** | `~/.agents/skills/skill-adapter/` | `<repo>/.agents/skills/<name>/` | Client trigger or prompt |

---

## Google Antigravity Notes (`agy` CLI, Antigravity IDE, Antigravity 2.0)

- **Workspace discovery & precedence:** Antigravity scans `<repo>/.agents/skills/` walking up from the current working directory to the repository root. Workspace-scoped skills take precedence over global skills in `~/.gemini/config/skills/`.
- **Skills vs. Rules (`GEMINI.md` / `AGENTS.md`):** Skills under `skills/<name>/SKILL.md` use progressive disclosure and load on demand. Standing rules in `GEMINI.md`, `AGENTS.md`, and `.agents/rules/*.md` are always active. When an external skill contains standing repo conventions, `skill-adapter` recommends those edits in your brief rather than silently editing rule files.

---

## Explicit Invocation (`disable-model-invocation: true`)

`skill-adapter` declares `disable-model-invocation: true` in its YAML frontmatter:

- **Zero idle context load:** Adapting an external skill is an intentional action, not an ambient coding rule. Disabling automatic model invocation ensures it never consumes prompt tokens during regular coding.
- **Explicit trigger:** Invoke it directly with `$skill-adapter` in Codex CLI, or mention it in your prompt (e.g., *"Use skill-adapter to adapt..."*).
- **Fallback for clients without slash commands:** If your client interface lacks command auto-completion for disabled-invocation skills, simply reference it in your prompt:

  ```text
  Read ~/.agents/skills/skill-adapter/SKILL.md and use it to adapt /path/to/external-skill for this repository.
  ```

---

## Installation Commands

### Option 1: Via `npx skills` (`skills.sh` / `agentskills.io` CLI)

```bash
npx skills add https://github.com/gcwillis14-coder/skill-adapter
```

### Option 2: Clone & Copy

```bash
git clone https://github.com/gcwillis14-coder/skill-adapter.git
cd skill-adapter
```

#### Tested Clients

```bash
# OpenAI Codex CLI / shared .agents/skills clients
mkdir -p ~/.agents/skills && cp -r skills/skill-adapter ~/.agents/skills/skill-adapter

# Google Antigravity (global)
mkdir -p ~/.gemini/config/skills && cp -r skills/skill-adapter ~/.gemini/config/skills/skill-adapter
```

#### Untested Clients

```bash
# Claude Code
mkdir -p ~/.claude/skills && cp -r skills/skill-adapter ~/.claude/skills/skill-adapter

# Cursor
mkdir -p ~/.cursor/skills && cp -r skills/skill-adapter ~/.cursor/skills/skill-adapter

# Windsurf
mkdir -p ~/.codeium/windsurf/skills && cp -r skills/skill-adapter ~/.codeium/windsurf/skills/skill-adapter

# GitHub Copilot (VS Code)
mkdir -p ~/.copilot/skills && cp -r skills/skill-adapter ~/.copilot/skills/skill-adapter
```

> [!NOTE]
> On POSIX systems where sandboxing allows reading external directories, you can substitute `cp -r` with `ln -s "$(pwd)/skills/skill-adapter" <target-path>` to receive updates automatically via `git pull`.

### Option 3: Workspace-Local Install (Single Project)

To install `skill-adapter` only inside a specific repository:

```bash
mkdir -p <repo>/.agents/skills
cp -r skills/skill-adapter <repo>/.agents/skills/skill-adapter
```

---

## Updating & Removing

### Updating `skill-adapter`

- **If copied (`cp -r`):** Pull changes in your clone and re-run the copy command.
- **If symlinked (`ln -s`):** Run `git pull` inside your `skill-adapter` clone directory.

### Uninstalling

Remove the directory or symlink:

```bash
rm -rf ~/.agents/skills/skill-adapter ~/.gemini/config/skills/skill-adapter
```

Project-local adapted skills previously generated inside your repositories remain completely self-contained and continue functioning independently.

---

## Input Formats `skill-adapter` Accepts

- **Local directory:** `/path/to/skill-dir` (or an existing installed skill folder)
- **GitHub repository or subdirectory URL:** `https://github.com/<owner>/<repo>` or `https://github.com/<owner>/<repo>/tree/main/skills/<name>`
- **Multi-skill / plugin bundle:** Repositories containing `plugin.json`, `.claude-plugin/`, `hooks/`, or multiple `skills/*/` folders (`skill-adapter` lists discovering skills and scopes which one to adapt)
- **Existing adapted skill (for updates):** Provide both the upstream source and your local adapted directory to run a three-way re-adaptation ([readapt-guide.md](../skills/skill-adapter/references/readapt-guide.md))

See [README.md](../README.md) for worked examples and [SCOPE.md](../SCOPE.md) for adaptation boundaries.
