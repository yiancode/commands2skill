# commands2skill

Convert [Claude Code](https://docs.anthropic.com/en/docs/claude-code) commands (`.md` files) to [Antigravity](https://blog.google/technology/google-deepmind/antigravity/) Skills format (folder + `SKILL.md` with YAML frontmatter).

English | [中文](README_CN.md)

The conversion is **lossless**: original content is preserved in full, with only the required YAML frontmatter header added.

## Quick Start

```bash
# Clone
git clone https://github.com/yiancode/commands2skill.git
cd commands2skill

# With Python 3.9+
python3 convert.py --input ~/.claude/commands --output ~/skills-output

# Without Python (Bash)
chmod +x convert.sh
./convert.sh ~/.claude/commands ~/skills-output
```

Then add `~/skills-output` to **Antigravity → Settings → Skill Custom Paths** and click Refresh.

## Why?

Claude Code uses **commands** — single `.md` files like `blog.md`, `video.md`.

Antigravity uses **skills** — folders containing a `SKILL.md` file with YAML frontmatter:

```
# Claude Command        →  Antigravity Skill
blog.md                 →  blog/SKILL.md
sc/analyze.md           →  sc-analyze/SKILL.md
```

This tool bridges the gap so you can use your Claude commands in Antigravity.

## Usage

### Option 1: Python (recommended)

```bash
# Convert all commands in a directory
python3 convert.py --input ~/.claude/commands --output ~/skills-output

# Convert a single file
python3 convert.py --input ~/.claude/commands/blog.md --output ~/skills-output

# Preview mode (no files written)
python3 convert.py --input ~/.claude/commands --output ~/skills-output --dry-run
```

Requires: Python 3.9+, no external dependencies.

### Option 2: Shell script (no Python needed)

```bash
# Make executable
chmod +x convert.sh

# Convert all commands
./convert.sh ~/.claude/commands ~/skills-output

# Preview mode
./convert.sh ~/.claude/commands ~/skills-output --dry-run
```

Requires: Bash only (built-in on macOS / Linux).

## Commit & Push

After converting, commit the output to Git to sync across machines:

```bash
# First time setup
cd ~/skills-output
git init
git remote add origin https://github.com/<your-username>/my-skills.git

# After updating commands, re-convert and push
python3 /path/to/commands2skill/convert.py \
  --input ~/.claude/commands \
  --output ~/skills-output

cd ~/skills-output
git add .
git commit -m "sync skills from commands $(date +%Y-%m-%d)"
git push origin main
```

> 💡 Tip: wrap the convert + commit + push steps into a `sync.sh` script so one command keeps everything in sync.

## What it does

For each `.md` command file:

1. Creates a folder named after the file (e.g., `blog.md` → `blog/`)
2. Generates `SKILL.md` inside that folder
3. Adds YAML frontmatter (`name` and `description`) at the top
4. Preserves the **entire original content** below the frontmatter

### Example

**Input** (`commands/blog.md`):
```markdown
# 技术博客生成

基于对话内容生成技术博客文章。
...
```

**Output** (`blog/SKILL.md`):
```markdown
---
name: blog
description: 技术博客生成。基于对话内容生成技术博客文章。
---

# 技术博客生成

基于对话内容生成技术博客文章。
...
```

## Subdirectory handling

Commands in subdirectories (e.g., `sc/analyze.md`) are converted with a prefix: `sc-analyze/SKILL.md`.

## Requirements

- **Python script**: Python 3.9+, no external dependencies
- **Shell script**: Bash (macOS / Linux built-in, Windows via Git Bash or WSL)

## License

MIT
