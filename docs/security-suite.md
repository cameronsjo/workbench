# Security Suite Plugin

OWASP compliance, vulnerability detection, and security auditing.

## Installation

```bash
/plugin install security-suite@cameron-tools
```

## Commands

### `/review.security`

Comprehensive security audit following OWASP Top 10.

**Usage:**
```bash
/review.security
/review.security src/auth/
```

**Checks:**
- OWASP Top 10 vulnerabilities
- Secret exposure
- Authentication/Authorization
- Input validation
- SQL injection
- XSS vulnerabilities
- CSRF protection
- Dependency vulnerabilities

## Agents

### security-auditor

Review code for vulnerabilities, implement secure authentication, and ensure OWASP compliance.

**Capabilities:**
- Vulnerability detection
- Auth implementation review
- JWT/OAuth2 patterns
- CORS/CSP configuration
- Encryption best practices

### api-security-audit

API-specific security review.

**Capabilities:**
- Authentication review
- Authorization checks
- Rate limiting
- Input validation
- Security header analysis

## Skills

### security-review

Security review checklists and patterns.

**Covers:**
- OWASP Top 10
- Secret detection patterns
- Secure coding guidelines
- Security headers
- Authentication patterns
- Authorization models

## Example Usage

### Run a Security Audit

```bash
/review.security
```

### Get Security Expertise

```
"Use security-auditor to review our authentication implementation"
"Check this API for security vulnerabilities"
```

### Design Secure Systems

```
"Following security-review patterns, design a secure session management system"
```

## Works Well With

- **api-development** - Secure API design
- **core-productivity** - Secure commits
- **cloud-ops** - Infrastructure security
