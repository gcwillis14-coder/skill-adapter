# Installation and Client Setup

The installable package is `skills/skill-adapter/`, containing SKILL.md, references, and a standard-library Python scanner. No MCP server, daemon, hook or build step is required. Python 3.10+ is required for Gate 1; development structural validation additionally requires PyYAML.

Prefer installing the adapter at user scope and the adapted output at project scope. Review the adapter before trusting its instructions or running its scanner.

## Compatibility status

The paths below are candidate conventions carried forward from the original setup guide, not live-client-verified guarantees. Confirm discovery, invocation and frontmatter support in your installed client/version. An agentskills.io-shaped directory does not establish identical behaviour across clients.

| Client | Candidate user path | Candidate project path | Invocation to verify |
| :--- | :--- | :--- | :--- |
| Claude Code | ~/.claude/skills/skill-adapter/ | .claude/skills/<name>/ | /skill-adapter |
| Codex CLI | ~/.agents/skills/skill-adapter/ | .agents/skills/<name>/ | $skill-adapter |
| Antigravity | ~/.gemini/config/skills/skill-adapter/ | .agents/skills/<name>/ | Explicit prompt/path if supported |

The adapter declares disable-model-invocation: true. This requests explicit invocation where supported; it is not a portable guarantee against automatic loading or idle context usage. No external client binaries were tested by the historical v1 evaluations. Claims about Antigravity aliases, precedence and always-on rule behaviour have not been established here.

## Copy installation

From the reviewed adapter repository:

```bash
git clone https://github.com/gcwillis14-coder/skill-adapter.git
cd skill-adapter

# Choose the location verified for your client; example for Claude Code:
mkdir -p ~/.claude/skills
cp -r skills/skill-adapter ~/.claude/skills/skill-adapter

# Alternative candidate for Codex:
# mkdir -p ~/.agents/skills
# cp -r skills/skill-adapter ~/.agents/skills/skill-adapter

# Antigravity candidate; verify discovery before using:
# mkdir -p ~/.gemini/config/skills
# cp -r skills/skill-adapter ~/.gemini/config/skills/skill-adapter
```

Use a fresh destination. Copying over an existing directory can retain obsolete files. For updates, stage a fresh copy, review changes and any local edits, then explicitly replace the old installation after checking the exact path. Do not blindly merge directory copies.

Symlinks are optional for this trusted adapter installation, but require platform support and may be inaccessible in sandboxes. This does not permit symlinks in imported source snapshots or adapted output.

## Invocation and trusted scanner path

Invoke by your client's supported command or explicitly read the trusted installed SKILL.md by absolute path. The adapter must resolve its scanner from that installation, never from the current repository or imported source:

```text
"/absolute/trusted/python3" -I -S "/absolute/trusted/skill-adapter/scripts/gate1_scan.py" "/absolute/private/source-snapshot" --json
```

Those are placeholders, not literal executable paths. Do not use an interpreter, scanner, virtual environment or wrapper supplied by the imported source. If trusted paths cannot be established, stop. Read the [security reference](../skills/skill-adapter/references/security-boundaries.md) for clean acquisition, content pinning, scanner limits and approval boundaries.

Scanner PASS is only hygiene. Every imported file still needs semantic review, and the model conducting that review can itself be targeted by prompt injection. Imported scripts are inspected as text, non-executable by default, and never run merely to validate them.

## Updates, re-adaptation and removal

Review adapter updates before replacing your trusted installation. For a symlinked trusted checkout, review the incoming Git changes rather than assuming every pull is safe.

When updating an adapted project skill, supply its installed version, the exact old upstream baseline and new pinned upstream. If the baseline cannot be recovered, disclose a two-way review. See [re-adaptation](../skills/skill-adapter/references/readapt-guide.md).

To uninstall, remove only the verified adapter directory or symlink you installed; do not run a blanket deletion across every client location. Already-generated project skills remain independent.

## Verification evidence

[Historical v1 results](../tests/results.md) cover EVAL-01–07 against an older skill, not this hardening revision. EVAL-08 exists as a fixture but has no result in that report. Behavioural evaluations and live Claude Code, Codex CLI or Antigravity compatibility have not been rerun for this revision. Scanner unit tests, structural validation and behavioural/live-client checks are distinct forms of evidence; passing one does not establish the others.
