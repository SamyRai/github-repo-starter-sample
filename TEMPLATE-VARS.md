# Template variables

This file lists common placeholders used across the template repository and where they should be replaced.

- `{{PROJECT_NAME}}` — human-friendly name; example: "My Project".
  Appears in `README.md`, badges, and documentation.
- `{{REPO_NAME}}` — repository name; example: `my-project`. Used in repository URLs and CI examples.
- `{{OWNER}}` — GitHub organization or owner; example: `example-org`.
- `{{YEAR}}` — copyright year; example: `2026`.
- `{{MAINTAINER_EMAIL}}` — primary contact for maintainer or team; example: `maintainer@example.com`.
- `{{PGP_KEY_URL}}` — optional PGP key URL for secure reporting (used by `SECURITY.md` examples).

How to replace placeholders

- Use `scripts/instantiate-template.sh` to replace values across repository files automatically.
- For small edits, update `CITATION.cff`, `README.md`, and `LICENSE` manually.
- Set repository-level Actions variables in Settings when a value should be configurable at the repo level rather than baked into files.
