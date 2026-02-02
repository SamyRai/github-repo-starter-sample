# Setup checklist

Follow these steps after creating a repository from this template to make the project ready for active development.

1. Replace placeholders
   - Update the common placeholders described in `TEMPLATE-VARS.md`.
   - Run the helper script (optional) to replace placeholders across files:

     ```bash
     ./scripts/instantiate-template.sh \
       --project-name "My Project" \
       --repo-name my-project \
       --owner my-org \
       --year 2026 \
       --maintainer-email me@example.com \
       --pgp-key-url ""
     ```

2. Update repository settings
   - Set repository-level **Actions variables** (Settings → Secrets and variables → Actions → Variables) used by workflows.
     For example, define `PACKAGE_NAME` in repository variables.
   - Configure required branch protection rules and default reviewers.

3. Check policy files
   - Edit `CITATION.cff`, `LICENSE`, `CODE_OF_CONDUCT.md`, and `SECURITY.md` to include project-specific contact details and owners.

4. CI / automation sanity checks
   - Confirm CI runs on the default branch (push a temporary commit to test).
   - Add `PACKAGE_NAME` (or other project variables) to repository Actions variables when appropriate.

5. Release process
   - Read `RELEASE.md` to learn the repository's release checklist and tagging/backport rules.

6. Optional: enable additional security contacts
   - If you maintain a PGP key for security contact, add `PGP_KEY_URL` in `TEMPLATE-VARS.md`.
     Also update `SECURITY.md` with an example encrypted report.

---

Quick troubleshooting

- If DCO fails: amend the latest commit with `git commit --amend -s --no-edit` then push.
  For multiple historic commits, use interactive rebase (`git rebase -i <commit>`) and add sign-offs as needed, then `git push --force-with-lease`.
- CLA problems: check the PR checks and the `cla-assistant` status in the PR checks tab.
