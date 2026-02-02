#!/usr/bin/env bash
set -euo pipefail

# Simple test for instantiate-template.sh
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Determine repository root based on this script's location
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

# Prepare
cp "$REPO_ROOT/scripts/instantiate-template.sh" "$TMPDIR/"
cat > "$TMPDIR/README.md" <<'EOF'
Project: {{PROJECT_NAME}}
EOF

cd "$TMPDIR"
chmod +x instantiate-template.sh
./instantiate-template.sh --project-name "Test Project"

if ! grep -q "Test Project" README.md; then
  echo "instantiate-template test failed: placeholder not replaced"
  exit 2
fi

echo "instantiate-template test passed"
