# Repository Template

Reusable repository template for open-source projects. It
includes recommended policy files, issue and PR templates, and example
GitHub Actions for CI and release automation.

[![CI](https://img.shields.io/badge/ci-passing-brightgreen)](https://github.com/<owner>/<repo>/actions)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Quick start

1. Clone: `git clone https://github.com/<owner>/<repo>.git`
2. Install (Node): `npm ci && npm test`
3. Install (Python):
   `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
4. Run tests: `npm test` or `pytest`
5. Run the setup checklist: follow `SETUP.md`.
Optionally run `./scripts/instantiate-template.py` to replace template placeholders.
   See `TEMPLATE-VARS.md` for placeholder definitions.

## What this repo contains

- Policy files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`

- Templates: issue and PR templates in `.github/` for consistent triage

- Automation examples: Dependabot and example CI workflows

## Maintainer status

This template is intended for general use. Replace contact emails, badges,
and placeholders with project-specific values when creating a new project
from this template.

## Community

See the project policies for contribution and support guidance:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [SECURITY.md](SECURITY.md)
- [SUPPORT.md](SUPPORT.md)

For questions, open an issue or use the repository Discussions tab if
enabled.
