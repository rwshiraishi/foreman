# Constitution template

One page, written by the boss before any dispatch. Every worker and checker prompt embeds it verbatim. Checkers grade against this document, not vibes. Amendments (from §7 disputes) are appended, dated, at the bottom.

```markdown
# Build constitution — <project> — <date>

## Stack facts
- Language/framework: <e.g. Next.js 15 + TypeScript, or static HTML/CSS>
- Build command: <exact command>   Test command: <exact command>   Lint: <exact command>
- Deploy target: <platform>; verification URL pattern: <url>

## Quality floor (checkers FAIL anything below this)
- Accessibility: <e.g. WCAG 2.2 AA — landmarks, contrast, focus order, meaningful alt text; test both themes>
- Security: no hardcoded secrets; inputs validated at boundaries; <project-specific>
- Tests: <coverage bar>; tests must actually run — a skipped test is a FAIL
- Style: <repo conventions; for Ray: no em dashes in copy, no AI cliches/hype words>

## Protected content (character-compared, never paraphrased)
- <list exact passages/quotes/legal text that must ship verbatim, with source of truth>

## Forbidden shortcuts (instant FAIL)
- Hidden/invisible elements to satisfy content checks
- Hardcoded expected values in place of real computation
- Mock/placeholder data standing in for missing real values (per CLAUDE.md)
- Disabling or skipping a check to pass it

## Verification commands by task type
- Code task: <build + test + lint commands; checker reads exit codes>
- Page task: <render/fetch command; both themes; key routes>
- Content task: <character-compare against protected-content list>

## Amendments
- <date>: <rubric change from arbitration, with reason>
```

## Worked example (static website, 10 lines)

```markdown
# Build constitution — author site — 2026-08-13
Stack: static HTML/CSS/JS, no framework. Build: none. Serve: python3 -m http.server.
Quality floor: WCAG 2.2 AA; Lighthouse a11y ≥ 95; works light+dark; no layout shift on fonts.
Protected: all author quotes in quotes.json — verbatim, curly quotes included.
Forbidden: invisible text, empty structural elements, lorem ipsum.
Verify (page): fetch each route, axe-core scan, screenshot both themes.
Verify (content): diff rendered quote text against quotes.json character-for-character.
```
