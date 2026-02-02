# Security Policy

Report security vulnerabilities privately to:

[security@glpx.pro](mailto:security@glpx.pro)

or open a private security issue on GitHub (choose "Security" and mark
private).

## What to include

Please provide:

- Affected versions (e.g., `v1.2.3`)

- Steps to reproduce and a minimal reproducible example (commands, code,
  logs)

- Impact assessment (what an attacker can do)

- Proof of concept (encrypt if sensitive)

## Encryption

Optionally encrypt sensitive attachments with the project PGP key:

[PGP key](https://example.com/pgp-key.asc) (placeholder) or PGP key ID `0xABCD1234`. Replace this placeholder when you publish your project's key.

Example: create an encrypted report and attach it to an issue or email:

```bash
# create a report
echo "Vulnerability report: details and repro steps" > report.txt
# encrypt for the project's PGP key
gpg --encrypt --recipient 0xABCD1234 --armor --output report.txt.asc report.txt
# attach the ASCII-armored file (report.txt.asc) to your report
```

## Response & disclosure

- Acknowledgement: within 72 hours

- Initial triage and severity assessment: within 7 business days

- We will coordinate disclosure and patches via GitHub Security Advisories
  or as agreed with the reporter.

If you require a CVE, indicate this in your report and we will work with you
to request one.
