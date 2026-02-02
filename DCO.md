# Developer Certificate of Origin (DCO)

This project requires a DCO sign-off on commits. The DCO confirms the
contributor has the right to submit work under the project's license.

How to sign your commits:

- Use `git commit -s -m "Your message"` to add a Signed-off-by line automatically.

- Or add a trailer manually:

  `Signed-off-by: Your Name <your-email@glpx.pro>`

If your PR fails the DCO check, add a sign-off to the missing commits with:

```bash
git commit --amend --no-edit -s
git push --force-with-lease
```

More info: see the [Developer Certificate of Origin](https://developercertificate.org/).
