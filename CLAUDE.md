# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

Sublime Text plugin that manages Windows classic context menu entries for Sublime Text/Merge via registry keys under HKCU. Windows-only, Python 3.14, Sublime Text build 4105+. Cannot be run as a standalone script — depends on the `sublime` and `sublime_plugin` modules available only inside Sublime Text's Python runtime. Type stubs live in `typings/` (sourced from ST-API-stubs repo, ST version 4136).

## Build & CI

- Package manager: **uv** only (not pip)
- Install deps: `uv sync`
- CI check (lint + type + format): `make ci-check`
- Auto-fix lint/format: `make ci-fix` (safe), `make ci-fix-unsafe` (includes unsafe fixes)

## Style

- Line length: 120
- Ruff handles all linting and formatting (rules: E, F, W, I, UP, FURB, SIM; isort single-line imports)
- Mypy for type checking (`check_untyped_defs = true`, `strict_optional = true`)
- EditorConfig: 4-space indentation for Python/JSON, 2-space for Markdown, tabs for Makefile
- `boot.py` is the entry point and may have E402 (module-level imports not at top — must reload previous modules first)

## Commit conventions

Types: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `style:`, `release:`
