#!/usr/bin/env python3
"""
Template instantiation script for GitHub repository templates.

This script replaces template placeholders with actual project values.
Designed to be run via GitHub Actions workflow after creating a repo
from template.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List


class TemplateInstantiator:
    """Handle template placeholder replacement across repository files."""

    # Files that should have placeholders replaced
    TARGET_FILES = [
        "README.md",
        "CITATION.cff",
        "LICENSE",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/ISSUE_TEMPLATE/security_report.yml",
        ".github/ISSUE_TEMPLATE/config.yml",
        ".github/CODEOWNERS",
        "SUPPORT.md",
        "SECURITY.md",
        "SECURITY_CONTACTS.md",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
    ]

    def __init__(self, root_dir: Path):
        """Initialize with repository root directory."""
        self.root_dir = root_dir

    def build_replacements(self, args: argparse.Namespace) -> Dict[str, str]:
        """Build placeholder to value mapping from arguments."""
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
        if args.support_email:
            replacements["{{SUPPORT_EMAIL}}"] = args.support_email
        if args.security_email:
            replacements["{{SECURITY_EMAIL}}"] = args.security_email
        if args.github_username:
            replacements["{{GITHUB_USERNAME}}"] = args.github_username
        if args.pgp_key_url:
            replacements["{{PGP_KEY_URL}}"] = args.pgp_key_url
        if args.pgp_key_id:
            replacements["{{PGP_KEY_ID}}"] = args.pgp_key_id

        return replacements

    def process_file(self, file_path: Path, replacements: Dict[str, str]) -> bool:
        """
        Process a single file, replacing placeholders.

        Returns True if file was modified, False otherwise.
        """
        if not file_path.exists():
            return False

        try:
            content = file_path.read_text(encoding="utf-8")
            original_content = content

            # Apply all replacements
            for placeholder, value in replacements.items():
                content = content.replace(placeholder, value)

            # Only write if content changed
            if content != original_content:
                file_path.write_text(content, encoding="utf-8")
                return True

            return False

        except (OSError, UnicodeDecodeError) as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)
            raise

    def instantiate(
        self, replacements: Dict[str, str], dry_run: bool = False
    ) -> List[Path]:
        """
        Instantiate template by replacing placeholders in target files.

        Returns list of files that were (or would be) modified.
        """
        modified_files = []

        for file_rel in self.TARGET_FILES:
            file_path = self.root_dir / file_rel

            if dry_run:
                if file_path.exists():
                    modified_files.append(file_path)
                    print(f"Would process: {file_rel}")
            else:
                if self.process_file(file_path, replacements):
                    modified_files.append(file_path)
                    print(f"✓ Updated: {file_rel}")

        return modified_files


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Replace template placeholders in repository files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Instantiate with all values
  %(prog)s --project-name "My Project" --repo-name "my-project" \\
    --owner "my-org" --year "2026" \\
    --maintainer-email "maintainer@example.com" \\
    --support-email "support@example.com" \\
    --security-email "security@example.com" \\
    --github-username "my-org/maintainers"

  # Dry run to see what would be changed
  %(prog)s --dry-run
        """,
    )

    parser.add_argument(
        "--project-name", help="Project name (replaces {{PROJECT_NAME}})"
    )
    parser.add_argument("--repo-name", help="Repository name (replaces {{REPO_NAME}})")
    parser.add_argument(
        "--owner", help="GitHub owner/organization (replaces {{OWNER}})"
    )
    parser.add_argument("--year", help="Copyright year (replaces {{YEAR}})")
    parser.add_argument(
        "--maintainer-email", help="Maintainer email (replaces {{MAINTAINER_EMAIL}})"
    )
    parser.add_argument(
        "--support-email", help="Support email (replaces {{SUPPORT_EMAIL}})"
    )
    parser.add_argument(
        "--security-email", help="Security email (replaces {{SECURITY_EMAIL}})"
    )
    parser.add_argument(
        "--github-username", help="GitHub username/team (replaces {{GITHUB_USERNAME}})"
    )
    parser.add_argument("--pgp-key-url", help="PGP key URL (replaces {{PGP_KEY_URL}})")
    parser.add_argument("--pgp-key-id", help="PGP key ID (replaces {{PGP_KEY_ID}})")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )
    parser.add_argument(
        "--root-dir",
        type=Path,
        default=Path.cwd(),
        help="Repository root directory (default: current directory)",
    )

    args = parser.parse_args()

    # Create instantiator and build replacements
    instantiator = TemplateInstantiator(args.root_dir)
    replacements = instantiator.build_replacements(args)

    if not replacements:
        print("No replacement values provided. Use --help for usage.", file=sys.stderr)
        sys.exit(1)

    # Perform instantiation
    try:
        modified = instantiator.instantiate(replacements, args.dry_run)

        if args.dry_run:
            print(f"\nDry run: {len(modified)} files would be modified")
        else:
            print(f"\n✓ Successfully modified {len(modified)} files")

    except Exception as e:
        print(f"\n✗ Error during instantiation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
