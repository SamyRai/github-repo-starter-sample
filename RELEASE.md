# Release checklist

Use this checklist when preparing a release.

1. Update changelog / release notes
   - Add a short summary of changes and the important user-facing items.

2. Bump version (if applicable)
   - Update project version in package files or tags.

3. Run full CI and ensure all checks pass

4. Tag release and push
   - `git tag -a vX.Y.Z -m "Release vX.Y.Z" && git push origin vX.Y.Z`

5. Create Release in GitHub
   - Use the Release Drafter draft or manually create a release with assets if needed.

6. Backport / hotfix
   - If the release needs backports, open PRs following the repository's backporting policy.

7. Announce release
   - Update communication channels (maintainer email list, website, or release notes) as appropriate.
