# Capability and Dependency Rules

Treat capabilities independently. Do not reduce the runtime to a named host or
a single local/non-local distinction.

Relevant capabilities include:

- filesystem access;
- Python 3.11+;
- PPTX writing;
- office rendering;
- PDF rendering;
- image inspection;
- image generation;
- visual inspection;
- CJK fonts.

When local Python exists, run `scripts/preflight.py`.

If a useful dependency is missing:

1. state what is missing and which step it improves;
2. ask whether the user wants it installed;
3. install only after confirmation;
4. if declined, use the strongest fallback;
5. record the missing capability and skipped checks in project state.

Do not ask about a missing optional dependency when it has no effect on the
requested outcome.
