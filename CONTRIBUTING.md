# Contributing to Dipex

Thanks for your interest in contributing! This document explains the workflow, coding style, and processes we use.

## How to contribute
1. Fork the repository (or clone if you have collaborator access).
2. Create a feature branch named `feat/<short-description>` or `fix/<short-description>`.
3. Make changes and run tests locally.
4. Open a Pull Request against `main` with a clear title and description.

## Branching and commits
- Use short, imperative commit messages (e.g., "Add OCR simulation" or "Fix user lookup in OCR endpoint").
- Squash related commits when the feature is complete.

## Coding style
- Python: follow PEP8. We use modern typing features and pydantic models.
- Use logging instead of print statements in backend code.

## Tests
- Add unit tests for new features where possible.
- Run tests locally before opening a PR.

## Pull request process
- Open a PR and reference related issues.
- Assign reviewers and wait for approvals before merging.
- Ensure the PR description lists what changed and how to test.

## Small tasks for newcomers
- See `TASKS.md` for suggested quick starter tasks labeled `good-first-issue`.
