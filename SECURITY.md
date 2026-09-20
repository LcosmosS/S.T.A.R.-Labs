# Security Policy

## Supported Versions

The S.T.A.R. Labs Research Program is an active research project. We currently support security updates for the **latest stable release** and the `main` branch.

| Version / Branch      | Supported          |
|-----------------------|--------------------|
| `main` (development)  | Yes                |
| Latest tagged release | Yes                |
| Older releases        | No                 |

## Reporting a Vulnerability

We take the security of this project seriously. If you discover a security vulnerability, please report it responsibly.

**Please do not report security vulnerabilities through public GitHub issues.**

### How to Report
- Email: security@ LcosmosS@pm.me (or open a **private** vulnerability report on GitHub if you prefer).
 
Please include **"S.T.A.R. Labs Research Program Security Report"** in the subject line and provide as much detail as possible, including:
  - Description of the vulnerability
  - Steps to reproduce
  - Potential impact
  - Any suggested mitigation

We aim to acknowledge receipt within **48 hours** and provide a full response (including estimated timeline for a fix) within **ASAP**.

## Scope

**In Scope**
- Vulnerabilities in the core Python/SageMath codebase (`src/`)
- Issues in the data processing and symbolic regression pipelines
- Security problems in the reproducible environment (`environment.yml`, `Dockerfile`)
- Vulnerabilities that could compromise research data integrity or reproducibility

**Out of Scope**
- Theoretical or mathematical weaknesses in the ACSC, ECC, or Symbolic Action Principle (these should be discussed as scientific critiques)
- Issues specific to external dependencies (SageMath, LMFDB, Gudhi, PySR, etc.) — please report those upstream
- Denial-of-service attacks on GitHub Actions or CI
- Social engineering or non-technical attacks

## Security Updates

When a security vulnerability is confirmed:
1. We will patch it as quickly as possible.
2. We will release a new version/tag with a clear security note in the changelog.
3. We will document the issue (without revealing exploit details until fixed) in the release notes.

## Acknowledgments

We greatly appreciate responsible security research that helps keep the S.T.A.R. Labs Research Program and the broader open-source scientific community secure.

Security researchers who report valid issues will be acknowledged in the release notes (unless anonymity is requested).
