# Contributing to TickioOSS

Thank you for your interest in contributing to TickioOSS! This document outlines the guidelines for contributing to this open-source project.

---

## Code of Conduct

Be respectful, inclusive, and constructive. Harassment or hostile behavior will not be tolerated.

---

## How to Contribute

### 1. Fork and clone

```bash
git clone https://github.com/YOUR_USERNAME/TickioOSS.git
cd TickioOSS
```

### 2. Create a branch

Use a descriptive branch name:

```bash
git checkout -b feature/ticket-attachments
git checkout -b fix/auth-token-expiry
git checkout -b docs/api-reference
```

### 3. Set up the development environment

```bash
# Backend
cd Backend
python -m venv venv && source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd ../Frontend
npm install
```

### 4. Make your changes

- Keep commits small and focused.
- Write meaningful commit messages (see format below).
- Add or update tests if you change backend logic.

### 5. Run tests

```bash
cd Backend
pytest tests/ -v
```

### 6. Open a Pull Request

- Base branch: `main`
- Fill in the PR description: what changed and why.
- Reference any related issues with `Fixes #<number>`.

---

## Commit Message Format

```
<type>(<scope>): <short description>

Types: feat, fix, docs, style, refactor, test, chore
```

Examples:
```
feat(tickets): add file attachment support
fix(auth): handle expired tokens correctly
docs(readme): update installation steps
test(tickets): add edge case for closed tickets
```

---

## Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, production-ready code |
| `feature/*` | New features |
| `fix/*` | Bug fixes |
| `docs/*` | Documentation changes |

---

## Code Style

### Python (Backend)
- Follow PEP 8.
- Use type hints everywhere.
- Format with `black` (optional but preferred).

### JavaScript / JSX (Frontend)
- Use functional components and hooks.
- Keep components under ~150 lines.
- No inline styles — use Tailwind classes.

---

## Reporting Issues

When opening an issue, include:
- Steps to reproduce
- Expected vs actual behavior
- OS, browser, Python/Node version

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
