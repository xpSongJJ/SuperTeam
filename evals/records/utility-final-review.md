All three prior findings are addressed:

- **Backticks:** Closing runs must match the opening run’s exact length, leaving the real missing link visible.
- **Quoted titles:** A closing parenthesis inside either quoted title form is consumed as title content.
- **Fences:** A closing fence permits only trailing spaces or tabs, so an info string prevents closure.

**One concrete blocker remains in the changed `LINK` matcher:** it silently skips a plain relative destination containing an apostrophe:

```markdown
[Broken](missing's.md)
```

The matcher requires every apostrophe to belong to a paired quoted segment, so this produces no destination and bypasses missing-file validation. The downstream destination parser accepts this non-whitespace relative URL; this does not require full CommonMark support.

Restrict title-quote handling to the optional title position and add a missing-file regression test for that example.

Static review only; no tools used. The reported 20 passing tests cover the three original examples but not this case.