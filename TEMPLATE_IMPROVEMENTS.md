# Template improvements & variables (recommendations)

Summary

- Sources: GitHub Docs (Actions contexts & variables, expressions, template repositories, issue/PR templates).

- Key capability: GitHub Actions provides multiple runtime contexts.

  Examples of contexts include: `github`, `env`, `vars`, `secrets`, `runner`, and
  `inputs`.

- Expression functions (examples): `format()`, `contains()`, `fromJSON()`.

- Note: template repositories are a convenient starting point for new
  projects. They do not automatically replace arbitrary placeholder text.

Quick findings

- Use Actions `vars` and workflow `env` to centralize project-level settings.
  This is helpful for CI and release behaviour. ✅

- Use issue forms (structured templates) and front-matter in issue templates to
  speed triage and reduce back-and-forth. ✅
- Template repositories do not auto-substitute arbitrary placeholders (for example, `{{PROJECT_NAME}}`).
  Provide a short setup step or small script that replaces placeholders after a
  repository is generated from the template. ⚠️

Recommended placeholders to document (kept as placeholders in the template)

- `{{PROJECT_NAME}}` — human-friendly name
- `{{REPO_NAME}}` — repository name
- `{{OWNER}}` — github owner/org
- `{{YEAR}}` — copyright year
- `{{MAINTAINER_EMAIL}}` — primary contact (you already keep `glpx.pro` addresses)
- `{{PGP_KEY_URL}}` — (optional) project's PGP key URL placeholder

For each placeholder, add a one-line instruction in a `SETUP.md` (or in
`README`) that tells the repo owner how and where to replace each placeholder
after creating a repository from the template.

Practical improvements & where to apply them

1. Setup / scaffolding (high impact)

   - Add `SETUP.md` with a short checklist for repository owners.

   - Optionally provide a helper script: `scripts/instantiate-template.sh`.
     The script can replace placeholders (sed or node) and configure local
     files such as the license owner, `CITATION.cff`, and README badges.

   - Add `TEMPLATE-VARS.md` listing placeholders and their expected values.

2. Templates & triage

   - Convert high-value issue templates to **issue forms** (YAML) to collect
     structured, validated input (required fields, choice lists).

   - Use template front-matter (`name`, `about`, `labels`, `assignees`) to
     set sensible defaults for triage.

   - Update `PULL_REQUEST_TEMPLATE.md` with an explicit checklist and a
     `Type` or `Category` field so automation can filter PRs for releases,
     docs, or urgent fixes.

3. Security & contact placeholders

   - Keep `security@glpx.pro` as the canonical security contact.

   - Document how to use the PGP key placeholder and include a short
     encrypted-report example in `SECURITY.md`.

   - Consider adding `SECURITY_CONTACTS.md` to list roles and rotation notes.

4. Actions & automation (CI / Dependabot / Auto-merge)

   - Use repository or organization-level **Actions variables** (Settings →
     Secrets and variables → Actions → Variables) to store project defaults.
     Reference them in workflows with `${{ vars.MY_VAR }}`.

   - Use `github`, `env`, and other contexts for run-time gates and checks.

   - Prefer expression helpers (`format()`, `case()`, `contains()`) to keep
     conditions readable.

   - Example guard for publication: `if: ${{ github.ref == 'refs/heads/main' }}`

5. CLA / DCO automation

   - Keep DCO check workflows and the CLA Assistant in place.

   - Add a one-line troubleshooting entry in `CONTRIBUTING.md` showing how
     to amend a commit to add a sign-off and how to verify CLA status.

Example snippets

- Reference a repo variable in a workflow (vars must be created in repository settings):

```yaml
env:
  PACKAGE_NAME: ${{ vars.PACKAGE_NAME }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building ${{ env.PACKAGE_NAME }}"
```

- Use `github` context to gate a job on branch:

```yaml
jobs:
  publish:
    if: ${{ github.ref == 'refs/heads/main' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "Publishing release from ${{ github.ref_name }}"
```

- Suggested issue form front-matter (YAML form, example):

```yaml
name: Bug report
about: File a bug so we can reproduce and fix it
labels: [bug, needs-triage]
body:
  - type: markdown
    attributes:
      value: |-
        Thanks for your report — fill the fields below with concrete steps.
  - type: input
    id: summary
    attributes:
      label: Summary
      description: Brief description of the problem
      placeholder: A short summary
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: Exact commands and environment
```

Note: the repo already uses `labels` and `status:` metadata.
Converting to issue forms improves consistency and allows required fields.

Operational checklist for adopting the changes

- Add `SETUP.md` and `TEMPLATE-VARS.md` describing placeholders and necessary replacements. ✅
- Offer a small `scripts/instantiate-template.sh` for convenience (optional but helpful). ✅
- Convert high-value issue templates to Issue Forms (bug, feature, security triage). ✅
- Add a short CI example using `${{ vars.* }}` showing how to override values at repo level. ✅
- Optionally add a `RELEASE.md` that contains a standard release checklist.
  Mention required labels and backport/tagging rules. ✅

References

- GitHub Actions: Contexts & variables — [Contexts reference](https://docs.github.com/en/actions/learn-github-actions/contexts)
- GitHub Actions: Expressions — [Expressions reference](https://docs.github.com/en/actions/learn-github-actions/expressions)
- Template repositories — [Template repositories docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)

---

## Implementation status ✅

I applied a first pass of the recommended improvements and added the following files and updates:

- **Added** `SETUP.md` — short setup checklist and quick troubleshooting. ✅
- **Added** `TEMPLATE-VARS.md` — documents recommended placeholders and usage. ✅
- **Added** `scripts/instantiate-template.sh` — small script to replace placeholders across core files (see `SETUP.md` for usage). ✅
- **Added** `RELEASE.md` — short release checklist. ✅
- **Added** `.github/workflows/publish-example.yml` — example workflow showing how to use `${{ vars.* }}` and branch gating. ✅
- **Updated** `README.md` — references `SETUP.md` and the instantiate script. ✅
- **Updated** `CONTRIBUTING.md` — added DCO/CLA troubleshooting commands. ✅

Next steps you might want me to take (pick any):

1. Make `scripts/instantiate-template.sh` executable and add tests for it. ✅
2. Add an example `SECURITY_CONTACTS.md` and an encrypted-report snippet in `SECURITY.md`. ⚠️
3. Replace legacy `.md` issue templates with short redirecters to the YAML Issue Forms (or keep them for older tooling). ⚠️

If you'd like, I can open a branch and create a PR with all these changes.
Reply with which of the optional items you'd like me to prioritize or say "open PR" and I'll prepare the branch and PR draft.
