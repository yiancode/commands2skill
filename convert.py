#!/usr/bin/env python3
"""commands2skill - Convert Claude Code commands to Antigravity Skills format.

Converts .md command files into skill folders with SKILL.md (YAML frontmatter + original content).
The conversion is lossless: original content is preserved in full.
"""

import argparse
import os
import re
import sys
from pathlib import Path


def extract_description(content: str) -> str:
    """Extract a description from the markdown content.

    Priority:
    1. First H1 heading text + first non-empty paragraph after it
    2. First non-empty line of text
    """
    lines = content.strip().split("\n")
    h1_text = ""
    first_para = ""

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        # Found H1 heading
        if stripped.startswith("# ") and not h1_text:
            h1_text = stripped[2:].strip()
            # Look for the first non-empty paragraph after H1
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if not next_line:
                    continue
                if next_line.startswith("#") or next_line.startswith("```") or next_line.startswith("---"):
                    break
                first_para = next_line
                break
            break
        # No H1 found yet, use first non-empty non-heading line
        elif not stripped.startswith("#") and not stripped.startswith("```") and not stripped.startswith("---"):
            first_para = stripped
            break

    if h1_text and first_para:
        desc = f"{h1_text}\u3002{first_para}" if not h1_text.endswith((".", "。", "!", "！", "?", "？")) else f"{h1_text} {first_para}"
    elif h1_text:
        desc = h1_text
    elif first_para:
        desc = first_para
    else:
        desc = "Converted from Claude Code command."

    # Truncate if too long (keep it reasonable for frontmatter)
    if len(desc) > 200:
        desc = desc[:197] + "..."

    return desc


def convert_command_to_skill(input_path: Path, output_dir: Path, prefix: str = "", dry_run: bool = False) -> list[str]:
    """Convert a single command .md file to a skill folder.

    Args:
        input_path: Path to the .md command file.
        output_dir: Base output directory for skills.
        prefix: Optional prefix for the skill name (for nested dirs).
        dry_run: If True, only print what would be done.

    Returns:
        List of actions taken (for logging).
    """
    actions = []
    name = input_path.stem  # filename without .md

    if prefix:
        skill_name = f"{prefix}-{name}"
    else:
        skill_name = name

    # Skip non-.md files and special files
    if input_path.suffix.lower() != ".md":
        return actions
    if name.startswith("."):
        return actions

    content = input_path.read_text(encoding="utf-8")
    description = extract_description(content)

    # Build SKILL.md content: YAML frontmatter + original content (lossless)
    frontmatter = f"---\nname: {skill_name}\ndescription: {description}\n---\n\n"
    skill_content = frontmatter + content

    skill_dir = output_dir / skill_name
    skill_file = skill_dir / "SKILL.md"

    if dry_run:
        actions.append(f"[DRY-RUN] Would create: {skill_file}")
        actions.append(f"          name: {skill_name}")
        actions.append(f"          description: {description[:80]}...")
    else:
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file.write_text(skill_content, encoding="utf-8")
        actions.append(f"[CREATED] {skill_file}")

    return actions


def convert_directory(input_dir: Path, output_dir: Path, prefix: str = "", dry_run: bool = False) -> list[str]:
    """Convert all commands in a directory (recursively) to skills.

    Args:
        input_dir: Directory containing .md command files.
        output_dir: Base output directory for skills.
        prefix: Optional prefix for nested directories.
        dry_run: If True, only print what would be done.

    Returns:
        List of all actions taken.
    """
    actions = []

    if not input_dir.is_dir():
        print(f"Error: {input_dir} is not a directory.", file=sys.stderr)
        return actions

    for item in sorted(input_dir.iterdir()):
        if item.name.startswith("."):
            continue

        if item.is_file() and item.suffix.lower() == ".md":
            actions.extend(convert_command_to_skill(item, output_dir, prefix, dry_run))
        elif item.is_dir():
            # Recurse into subdirectories with prefix
            sub_prefix = f"{prefix}-{item.name}" if prefix else item.name
            actions.extend(convert_directory(item, output_dir, sub_prefix, dry_run))

    return actions


def main():
    parser = argparse.ArgumentParser(
        description="Convert Claude Code commands (.md) to Antigravity Skills format.",
        epilog="Example: python convert.py --input ~/.claude/commands --output ~/skills-output",
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input path: a commands directory or a single .md file.",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output directory for generated skills.",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Preview mode: show what would be done without writing files.",
    )
    parser.add_argument(
        "--prefix", "-p",
        default="",
        help="Optional prefix for skill names.",
    )

    args = parser.parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()

    if not input_path.exists():
        print(f"Error: Input path does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input:  {input_path}")
    print(f"Output: {output_dir}")
    print(f"Mode:   {'DRY-RUN (preview only)' if args.dry_run else 'CONVERT'}")
    print("---")

    if input_path.is_file():
        actions = convert_command_to_skill(input_path, output_dir, args.prefix, args.dry_run)
    elif input_path.is_dir():
        actions = convert_directory(input_path, output_dir, args.prefix, args.dry_run)
    else:
        print(f"Error: {input_path} is neither a file nor a directory.", file=sys.stderr)
        sys.exit(1)

    for action in actions:
        print(action)

    print("---")
    count = len([a for a in actions if "[CREATED]" in a or "[DRY-RUN]" in a])
    print(f"Total: {count} skill(s) {'would be created' if args.dry_run else 'created'}.")


if __name__ == "__main__":
    main()
