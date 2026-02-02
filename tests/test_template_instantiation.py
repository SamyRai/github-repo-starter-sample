#!/usr/bin/env python3
"""
Unit tests for template instantiation script.

Run with: python -m pytest tests/test_template_instantiation.py -v
Or: python tests/test_template_instantiation.py
"""

import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path to import the script
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from instantiate_template import TemplateInstantiator  # noqa: E402


class TestTemplateInstantiator(unittest.TestCase):
    """Test cases for TemplateInstantiator class."""

    def setUp(self):
        """Create temporary directory for each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.instantiator = TemplateInstantiator(self.root)

    def tearDown(self):
        """Clean up temporary directory."""
        self.temp_dir.cleanup()

    def test_single_placeholder_replacement(self):
        """Test replacing a single placeholder in a file."""
        test_file = self.root / "README.md"
        test_file.write_text("# {{PROJECT_NAME}}\n")

        replacements = {"{{PROJECT_NAME}}": "My Project"}
        modified = self.instantiator.process_file(test_file, replacements)

        self.assertTrue(modified)
        self.assertEqual(test_file.read_text(), "# My Project\n")

    def test_multiple_placeholder_replacement(self):
        """Test replacing multiple placeholders in a file."""
        test_file = self.root / "README.md"
        test_file.write_text(
            "# {{PROJECT_NAME}}\n" "Owner: {{OWNER}}\n" "Year: {{YEAR}}\n"
        )

        replacements = {
            "{{PROJECT_NAME}}": "Test Project",
            "{{OWNER}}": "test-org",
            "{{YEAR}}": "2026",
        }
        modified = self.instantiator.process_file(test_file, replacements)

        self.assertTrue(modified)
        content = test_file.read_text()
        self.assertIn("# Test Project", content)
        self.assertIn("Owner: test-org", content)
        self.assertIn("Year: 2026", content)

    def test_no_changes_when_no_placeholders(self):
        """Test that files without placeholders are not modified."""
        test_file = self.root / "README.md"
        original_content = "# Regular Project\nNo placeholders here\n"
        test_file.write_text(original_content)

        replacements = {"{{PROJECT_NAME}}": "My Project"}
        modified = self.instantiator.process_file(test_file, replacements)

        self.assertFalse(modified)
        self.assertEqual(test_file.read_text(), original_content)

    def test_email_placeholders(self):
        """Test replacing email-related placeholders."""
        test_file = self.root / "SUPPORT.md"
        test_file.write_text(
            "Support: {{SUPPORT_EMAIL}}\n"
            "Security: {{SECURITY_EMAIL}}\n"
            "Maintainer: {{MAINTAINER_EMAIL}}\n"
        )

        replacements = {
            "{{SUPPORT_EMAIL}}": "support@example.com",
            "{{SECURITY_EMAIL}}": "security@example.com",
            "{{MAINTAINER_EMAIL}}": "maintainer@example.com",
        }
        modified = self.instantiator.process_file(test_file, replacements)

        self.assertTrue(modified)
        content = test_file.read_text()
        self.assertIn("support@example.com", content)
        self.assertIn("security@example.com", content)
        self.assertIn("maintainer@example.com", content)

    def test_codeowners_placeholder(self):
        """Test replacing GitHub username in CODEOWNERS."""
        github_dir = self.root / ".github"
        github_dir.mkdir(parents=True)
        test_file = github_dir / "CODEOWNERS"
        test_file.write_text("* @{{GITHUB_USERNAME}}\n")

        replacements = {"{{GITHUB_USERNAME}}": "my-org/maintainers"}
        modified = self.instantiator.process_file(test_file, replacements)

        self.assertTrue(modified)
        self.assertIn("@my-org/maintainers", test_file.read_text())

    def test_pgp_placeholders(self):
        """Test replacing PGP key placeholders."""
        test_file = self.root / "SECURITY.md"
        test_file.write_text("PGP Key: {{PGP_KEY_URL}}\n" "Key ID: {{PGP_KEY_ID}}\n")

        replacements = {
            "{{PGP_KEY_URL}}": "https://example.com/key.asc",
            "{{PGP_KEY_ID}}": "0xABCD1234",
        }
        modified = self.instantiator.process_file(test_file, replacements)

        self.assertTrue(modified)
        content = test_file.read_text()
        self.assertIn("https://example.com/key.asc", content)
        self.assertIn("0xABCD1234", content)

    def test_nonexistent_file_returns_false(self):
        """Test that processing a nonexistent file returns False."""
        test_file = self.root / "nonexistent.md"
        replacements = {"{{PROJECT_NAME}}": "Test"}

        modified = self.instantiator.process_file(test_file, replacements)
        self.assertFalse(modified)

    def test_dry_run_does_not_modify_files(self):
        """Test that dry run mode doesn't actually modify files."""
        test_file = self.root / "README.md"
        original = "# {{PROJECT_NAME}}\n"
        test_file.write_text(original)

        replacements = {"{{PROJECT_NAME}}": "Test Project"}

        # Run in dry-run mode
        modified = self.instantiator.instantiate(replacements, dry_run=True)

        # File should not be modified
        self.assertEqual(test_file.read_text(), original)
        # But should report it would be modified
        self.assertEqual(len(modified), 1)

    def test_discussion_url_replacement(self):
        """Test replacing discussion URL with owner and repo."""
        github_dir = self.root / ".github" / "ISSUE_TEMPLATE"
        github_dir.mkdir(parents=True)
        test_file = github_dir / "config.yml"
        test_file.write_text(
            "url: https://github.com/{{OWNER}}/{{REPO_NAME}}/discussions\n"
        )

        replacements = {
            "{{OWNER}}": "my-org",
            "{{REPO_NAME}}": "my-repo",
        }
        modified = self.instantiator.process_file(test_file, replacements)

        self.assertTrue(modified)
        self.assertIn(
            "https://github.com/my-org/my-repo/discussions", test_file.read_text()
        )

    def test_unicode_content_handling(self):
        """Test that Unicode content is handled correctly."""
        test_file = self.root / "README.md"
        test_file.write_text(
            "# {{PROJECT_NAME}} 🚀\n" "Powered by ❤️\n" "Copyright © {{YEAR}}\n",
            encoding="utf-8",
        )

        replacements = {
            "{{PROJECT_NAME}}": "Test Project",
            "{{YEAR}}": "2026",
        }
        modified = self.instantiator.process_file(test_file, replacements)

        self.assertTrue(modified)
        content = test_file.read_text(encoding="utf-8")
        self.assertIn("Test Project 🚀", content)
        self.assertIn("Copyright © 2026", content)


class TestIntegration(unittest.TestCase):
    """Integration tests for full workflow."""

    def setUp(self):
        """Create temporary directory for each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.instantiator = TemplateInstantiator(self.root)

    def tearDown(self):
        """Clean up temporary directory."""
        self.temp_dir.cleanup()

    def test_full_instantiation_workflow(self):
        """Test complete instantiation workflow with multiple files."""
        # Create test files
        readme = self.root / "README.md"
        readme.write_text(
            "# {{PROJECT_NAME}}\n" "Repository: {{OWNER}}/{{REPO_NAME}}\n"
        )

        support = self.root / "SUPPORT.md"
        support.write_text("Contact: {{SUPPORT_EMAIL}}\n")

        github_dir = self.root / ".github"
        github_dir.mkdir()
        codeowners = github_dir / "CODEOWNERS"
        codeowners.write_text("* @{{GITHUB_USERNAME}}\n")

        # Perform instantiation
        replacements = {
            "{{PROJECT_NAME}}": "My Project",
            "{{OWNER}}": "my-org",
            "{{REPO_NAME}}": "my-repo",
            "{{SUPPORT_EMAIL}}": "support@example.com",
            "{{GITHUB_USERNAME}}": "my-org/team",
        }

        modified = self.instantiator.instantiate(replacements)

        # Verify all files were modified
        self.assertEqual(len(modified), 3)

        # Verify content
        self.assertIn("# My Project", readme.read_text())
        self.assertIn("my-org/my-repo", readme.read_text())
        self.assertIn("support@example.com", support.read_text())
        self.assertIn("@my-org/team", codeowners.read_text())


if __name__ == "__main__":
    unittest.main()
