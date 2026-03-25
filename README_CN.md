# commands2skill

将 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的 commands（`.md` 文件）无损转换为 [Antigravity](https://blog.google/technology/google-deepmind/antigravity/) 的 Skills 格式。

[English](README.md) | 中文

## 为什么需要这个工具？

Claude Code 使用 **commands** —— 单个 `.md` 文件（如 `blog.md`、`video.md`）。

Antigravity 使用 **skills** —— 文件夹内包含带 YAML frontmatter 的 `SKILL.md` 文件。

两者格式不兼容，这个工具帮你一键转换：

```
Claude Command           →  Antigravity Skill
blog.md                  →  blog/SKILL.md
sc/analyze.md            →  sc-analyze/SKILL.md
```

## 转换是无损的

- ✅ 原始内容 **完整保留**，一个字都不改
- ✅ 仅在顶部添加 3 行 YAML frontmatter（`name` + `description`），这是 Antigravity 识别 skill 的最低要求
- ✅ 子目录结构自动处理

## 快速开始

### 方式一：Python 脚本（推荐）

```bash
# 转换所有 commands
python3 convert.py --input ~/.claude/commands --output ~/skills-output

# 转换单个文件
python3 convert.py --input ~/.claude/commands/blog.md --output ~/skills-output

# 预览模式（不写入文件，只显示会做什么）
python3 convert.py --input ~/.claude/commands --output ~/skills-output --dry-run
```

要求：Python 3.9+，无需安装任何依赖。

### 方式二：Shell 脚本（无需 Python）

```bash
# 添加执行权限
chmod +x convert.sh

# 转换所有 commands
./convert.sh ~/.claude/commands ~/skills-output

# 预览模式
./convert.sh ~/.claude/commands ~/skills-output --dry-run
```

仅需 Bash，macOS / Linux 自带，无需安装任何东西。

## 转换示例

**输入** `commands/blog.md`：
```markdown
# 技术博客生成

基于对话内容生成技术博客文章。
...
```

**输出** `blog/SKILL.md`：
```markdown
---
name: blog
description: 技术博客生成。基于对话内容生成技术博客文章。
---

# 技术博客生成

基于对话内容生成技术博客文章。
...
```

↑ 原始内容在 `---` 下方，一字不差。

## 转换后怎么用？

1. 打开 Antigravity 设置页（Settings → Customizations）
2. 在 **Skill Custom Paths** 中点 **+ Add**
3. 添加你的输出目录路径（如 `~/skills-output`）
4. 点 **Refresh**，你的 commands 就变成可用的 skills 了

## 子目录处理

如果你的 commands 目录有子目录（如 `sc/`），里面的文件会以 `{目录名}-{文件名}` 命名：

```
sc/analyze.md    →  sc-analyze/SKILL.md
sc/build.md      →  sc-build/SKILL.md
```

## 常见问题

**Q: 转换后原始 commands 会被修改吗？**
A: 不会。这是单向复制转换，原始文件完全不动。

**Q: 可以重复运行吗？**
A: 可以。已存在的 skill 会被覆盖为最新版本。

**Q: 支持 Windows 吗？**
A: Python 脚本支持。Shell 脚本需要 Git Bash 或 WSL。

## License

MIT
