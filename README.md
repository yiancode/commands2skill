# commands2skill

Convert [Claude Code](https://docs.anthropic.com/en/docs/claude-code) commands (`.md` files) to [Antigravity](https://blog.google/technology/google-deepmind/antigravity/) Skills format (folder + `SKILL.md` with YAML frontmatter).

The conversion is **lossless**: original content is preserved in full, with only the required YAML frontmatter header added.

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

```bash
# Convert all commands in a directory
python convert.py --input ~/.claude/commands --output ~/skills-output

# Convert a single file
python convert.py --input ~/.claude/commands/blog.md --output ~/skills-output

# Preview mode (no files written)
python convert.py --input ~/.claude/commands --output ~/skills-output --dry-run
```

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

- Python 3.9+
- No external dependencies

## License

MIT
