#!/usr/bin/env python3
"""
Simple instantiate script to replace common placeholders in files.

Usage examples:
  ./scripts/instantiate-template.py --project-name "My Project" --repo-name my-project --owner my-org --year 2026 --maintainer-email me@example.com
  ./scripts/instantiate-template.py --dry-run
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Replace template placeholders in files"
    )
    parser.add_argument(
        "--project-name", help="Project name to substitute for {{PROJECT_NAME}}"
    )
    parser.add_argument(
        "--repo-name", help="Repository name to substitute for {{REPO_NAME}}"
    )
    parser.add_argument(
        "--owner", help="GitHub owner/organization to substitute for {{OWNER}}"
    )
    parser.add_argument("--year", help="Year to substitute for {{YEAR}}")
    parser.add_argument(
        "--maintainer-email", help="Email to substitute for {{MAINTAINER_EMAIL}}"
    )
    parser.add_argument(
        "--pgp-key-url", help="PGP key URL to substitute for {{PGP_KEY_URL}}"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show files that would be changed"
    )

    args = parser.parse_args()

    # Files to update (restrict to common files to avoid accidental changes)
    files = [
        "README.md",
        "CITATION.cff",
        "LICENSE",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
    ]

    # Build replacement map
    replacements = {}
    if args.project_name:
        replacements["{{PROJECT_NAME}}"] = args.project_name
    if args.repo_name:
        replacements["{{REPO_NAME}}"] = args.repo_name
    if args.owner:
        replacements["{{OWNER}}"] = args.owner
    if args.year:
        replacements["{{YEAR}}"] = args.year
    if args.maintainer_email:
        replacements["{{MAINTAINER_EMAIL}}"] = args.maintainer_email
    if args.pgp_key_url:
        replacements["{{PGP_KEY_URL}}"] = args.pgp_key_url

    if args.dry_run:
        print("Dry run enabled — files that would be changed:")
        for file_path in files:
            if Path(file_path).exists():
                print(f" - {file_path}")
        sys.exit(0)

    # Perform replacements
    for file_path in files:
        path = Path(file_path)
        if not path.exists():
            continue

        print(f"Processing {file_path}", flush=True)
        try:
            content = path.read_text(encoding="utf-8")

            # Apply all replacements
            for placeholder, value in replacements.items():
                content = content.replace(placeholder, value)

            path.write_text(content, encoding="utf-8")
            print(f"  ✓ Updated {file_path}", flush=True)
        except (OSError, UnicodeDecodeError) as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr, flush=True)
            sys.exit(1)

    print(
        "Done. If you updated files, review changes and commit them (e.g., git add . && git commit -m 'Instantiate template placeholders')."
    )


if __name__ == "__main__":
    main()
