#!/usr/bin/env bash
set -euo pipefail

# Simple instantiate script to replace common placeholders in files.
# Usage examples:
#  ./scripts/instantiate-template.sh --project-name "My Project" --repo-name my-project --owner my-org --year 2026 --maintainer-email me@example.com
#  ./scripts/instantiate-template.sh --dry-run

show_help() {
  cat <<-EOF
Usage: $0 [options]

Options:
  --project-name VALUE    Project name to substitute for {{PROJECT_NAME}}
  --repo-name VALUE       Repository name to substitute for {{REPO_NAME}}
  --owner VALUE           GitHub owner/organization to substitute for {{OWNER}}
  --year VALUE            Year to substitute for {{YEAR}}
  --maintainer-email VAL  Email to substitute for {{MAINTAINER_EMAIL}}
  --pgp-key-url VAL       PGP key URL to substitute for {{PGP_KEY_URL}}
  --dry-run               Show files that would be changed
  -h, --help              Show this help
EOF
}

# Defaults
DRY_RUN=0
PROJECT_NAME=""
REPO_NAME=""
OWNER=""
YEAR=""
MAINTAINER_EMAIL=""
PGP_KEY_URL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-name) PROJECT_NAME="$2"; shift 2;;
    --repo-name) REPO_NAME="$2"; shift 2;;
    --owner) OWNER="$2"; shift 2;;
    --year) YEAR="$2"; shift 2;;
    --maintainer-email) MAINTAINER_EMAIL="$2"; shift 2;;
    --pgp-key-url) PGP_KEY_URL="$2"; shift 2;;
    --dry-run) DRY_RUN=1; shift 1;;
    -h|--help) show_help; exit 0;;
    *) echo "Unknown option: $1"; show_help; exit 1;;
  esac
done

# Prepare replacements (we will use Perl's \Q...\E to quote replacements in the substitution)
REPL_PROJECT_NAME="$PROJECT_NAME"
REPL_REPO_NAME="$REPO_NAME"
REPL_OWNER="$OWNER"
REPL_YEAR="$YEAR"
REPL_MAINTAINER_EMAIL="$MAINTAINER_EMAIL"
REPL_PGP_KEY_URL="$PGP_KEY_URL"

# Files to update (restrict to common files to avoid accidental changes)
FILES=(
  README.md
  CITATION.cff
  LICENSE
  .github/PULL_REQUEST_TEMPLATE.md
  .github/ISSUE_TEMPLATE/bug_report.md
  .github/ISSUE_TEMPLATE/feature_request.md
)

if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run enabled — files that would be changed:"
  for f in "${FILES[@]}"; do
    if [[ -f $f ]]; then
      echo " - $f"
    fi
  done
  exit 0
fi

# Perform replacement where provided
for f in "${FILES[@]}"; do
  [[ -f $f ]] || continue
  echo "Processing $f"
  [[ -n "$PROJECT_NAME" ]] && perl -0777 -pe "s|\{\{PROJECT_NAME\}\}|\Q$REPL_PROJECT_NAME\E|g" -i.bak "$f" && rm -f "$f.bak"
  [[ -n "$REPO_NAME" ]] && perl -0777 -pe "s|\{\{REPO_NAME\}\}|\Q$REPL_REPO_NAME\E|g" -i.bak "$f" && rm -f "$f.bak"
  [[ -n "$OWNER" ]] && perl -0777 -pe "s|\{\{OWNER\}\}|\Q$REPL_OWNER\E|g" -i.bak "$f" && rm -f "$f.bak"
  [[ -n "$YEAR" ]] && perl -0777 -pe "s|\{\{YEAR\}\}|\Q$REPL_YEAR\E|g" -i.bak "$f" && rm -f "$f.bak"
  [[ -n "$MAINTAINER_EMAIL" ]] && perl -0777 -pe "s|\{\{MAINTAINER_EMAIL\}\}|\Q$REPL_MAINTAINER_EMAIL\E|g" -i.bak "$f" && rm -f "$f.bak"
  [[ -n "$PGP_KEY_URL" ]] && perl -0777 -pe "s|\{\{PGP_KEY_URL\}\}|\Q$REPL_PGP_KEY_URL\E|g" -i.bak "$f" && rm -f "$f.bak"
done

echo "Done. If you updated files, review changes and commit them (e.g., git add . && git commit -m 'Instantiate template placeholders')."
