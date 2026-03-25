#!/usr/bin/env bash
#
# commands2skill - Convert Claude Code commands to Antigravity Skills format.
# Shell script version for users without Python.
#
# Usage:
#   ./convert.sh <input_dir> <output_dir> [--dry-run]
#
# Examples:
#   ./convert.sh ~/.claude/commands ~/skills-output
#   ./convert.sh ~/.claude/commands ~/skills-output --dry-run
#

set -euo pipefail

# --- Argument parsing ---
if [ $# -lt 2 ]; then
    echo "Usage: $0 <input_dir> <output_dir> [--dry-run]"
    echo ""
    echo "Convert Claude Code commands (.md) to Antigravity Skills format."
    echo ""
    echo "Arguments:"
    echo "  input_dir    Directory containing .md command files"
    echo "  output_dir   Output directory for generated skills"
    echo "  --dry-run    Preview mode, don't write any files"
    echo ""
    echo "Examples:"
    echo "  $0 ~/.claude/commands ~/skills-output"
    echo "  $0 ~/.claude/commands ~/skills-output --dry-run"
    exit 1
fi

INPUT_DIR="$(cd "$1" && pwd)"
OUTPUT_DIR="$2"
DRY_RUN=false

if [ "${3:-}" = "--dry-run" ]; then
    DRY_RUN=true
fi

# --- Helper functions ---

# Extract description from markdown content.
# Uses first H1 heading + first paragraph after it.
extract_description() {
    local file="$1"
    local h1=""
    local first_para=""
    local found_h1=false

    while IFS= read -r line; do
        # Skip empty lines before finding content
        [ -z "$(echo "$line" | tr -d '[:space:]')" ] && continue

        # Found H1 heading
        if [[ "$line" =~ ^#\ (.+) ]] && [ "$found_h1" = false ]; then
            h1="${BASH_REMATCH[1]}"
            found_h1=true
            continue
        fi

        # After H1, find first non-empty, non-heading paragraph
        if [ "$found_h1" = true ] && [ -z "$first_para" ]; then
            # Skip headings, code blocks, horizontal rules
            [[ "$line" =~ ^# ]] && break
            [[ "$line" =~ ^\`\`\` ]] && break
            [[ "$line" =~ ^--- ]] && break
            first_para="$(echo "$line" | sed 's/^[[:space:]]*//')"
            break
        fi

        # No H1 found, use first non-special line
        if [ "$found_h1" = false ]; then
            [[ "$line" =~ ^# ]] && continue
            [[ "$line" =~ ^\`\`\` ]] && continue
            [[ "$line" =~ ^--- ]] && continue
            first_para="$(echo "$line" | sed 's/^[[:space:]]*//')"
            break
        fi
    done < "$file"

    if [ -n "$h1" ] && [ -n "$first_para" ]; then
        echo "${h1}。${first_para}"
    elif [ -n "$h1" ]; then
        echo "$h1"
    elif [ -n "$first_para" ]; then
        echo "$first_para"
    else
        echo "Converted from Claude Code command."
    fi
}

# Convert a single .md file to a skill folder
convert_file() {
    local file="$1"
    local output_base="$2"
    local prefix="$3"

    local basename="$(basename "$file" .md)"

    # Skip dotfiles
    [[ "$basename" =~ ^\. ]] && return

    local skill_name="$basename"
    if [ -n "$prefix" ]; then
        skill_name="${prefix}-${basename}"
    fi

    local description
    description="$(extract_description "$file")"

    # Truncate description if too long
    if [ ${#description} -gt 200 ]; then
        description="${description:0:197}..."
    fi

    local skill_dir="${output_base}/${skill_name}"
    local skill_file="${skill_dir}/SKILL.md"

    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would create: ${skill_file}"
        echo "          name: ${skill_name}"
        echo "          description: ${description:0:80}..."
    else
        mkdir -p "$skill_dir"
        # Write YAML frontmatter + original content (lossless)
        {
            echo "---"
            echo "name: ${skill_name}"
            echo "description: ${description}"
            echo "---"
            echo ""
            cat "$file"
        } > "$skill_file"
        echo "[CREATED] ${skill_file}"
    fi
}

# --- Main ---

echo "Input:  ${INPUT_DIR}"
echo "Output: ${OUTPUT_DIR}"
echo "Mode:   $([ "$DRY_RUN" = true ] && echo 'DRY-RUN (preview only)' || echo 'CONVERT')"
echo "---"

COUNT=0

# Process top-level .md files
for f in "${INPUT_DIR}"/*.md; do
    [ -f "$f" ] || continue
    convert_file "$f" "$OUTPUT_DIR" ""
    COUNT=$((COUNT + 1))
done

# Process subdirectories
for d in "${INPUT_DIR}"/*/; do
    [ -d "$d" ] || continue
    dir_name="$(basename "$d")"
    [[ "$dir_name" =~ ^\. ]] && continue

    for f in "${d}"*.md; do
        [ -f "$f" ] || continue
        convert_file "$f" "$OUTPUT_DIR" "$dir_name"
        COUNT=$((COUNT + 1))
    done
done

echo "---"
echo "Total: ${COUNT} skill(s) $([ "$DRY_RUN" = true ] && echo 'would be created' || echo 'created')."
