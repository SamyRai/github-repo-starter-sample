# Contributing

Thank you for contributing. This document describes the developer
workflow, PR expectations, and project checks to ensure timely, consistent
reviews.

## Development setup

1. Fork the repository and create a branch:
   `git checkout -b feat/short-description` or `fix/short-description`.

2. Follow setup in `README.md` and install dependencies.

3. Run tests and linters before committing:

   - Node: `npm ci && npm test && npm run lint`

   - Python:
     `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && pytest`

## Workflow

- Open an issue for non-trivial changes to discuss scope and design.

- Keep PRs focused and small to simplify review.

- Write tests for new behavior and update existing tests as needed.

- Commit messages should follow conventional commits (e.g., `fix:`, `feat:`).

- Branch naming: `feat/<short>`, `fix/<short>`, `chore/<task>`.

## Pull request checklist

Before requesting a review, ensure the PR includes:

- [ ] A concise summary of changes and linked issue (if applicable)

- [ ] Tests added/updated and passing locally (`npm test` / `pytest`)

- [ ] Linting passed (`npm run lint`)

- [ ] DCO sign-off on commits (`Signed-off-by:`)

- [ ] CLA signed (or signature pending)

- [ ] Changelog or release note entry when appropriate

## DCO & CLA

- DCO: Sign commits with `git commit -s -m "Message"` or add a `Signed-off-by:` trailer manually.

- If a PR fails the DCO check: amend the latest commit with `git commit --amend -s --no-edit` and push; for multiple historic commits, use interactive rebase (`git rebase -i <commit>`) and add the sign-off to each commit, then `git push --force-with-lease`.

- CLA: Sign via [cla-assistant](https://cla-assistant.io) when prompted. To verify CLA status, check the PR checks — the CLA Assistant will report success/failure in the checks tab.

- For offline signings or legal questions, contact [legal@glpx.pro](mailto:legal@glpx.pro).

## Reviews & Maintainers

- Assign reviewers using the repository's CODEOWNERS or by tagging maintainers in the PR.

- Review turnaround: maintainers respond to review requests within 1–3 business days.

- Keep PRs updated with the base branch to avoid merge conflicts.

## Automation

- Dependabot updates may be auto-merged when CI and policy checks pass.

- CI must pass and required checks must be green for merges.
