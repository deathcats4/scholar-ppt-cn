# CJK Typography Rules

Use role-based typography.

1. Prefer font roles extracted from the user template.
2. Keep title, heading, body, caption, source-note, and emphasis roles distinct.
3. Use bold only where the role or content requires emphasis.
4. Use a platform-aware fallback stack, for example:
   - Microsoft YaHei;
   - PingFang SC;
   - Source Han Sans SC;
   - Noto Sans CJK SC.
5. Check locally available fonts before construction when possible.
6. Keep mixed-language runs together when splitting them would damage baseline,
   spacing, or editability.
7. Do not modify text baked into source images.

QA for missing fonts, substitution, unreadable sizes, and lost hierarchy. Do not
require every CJK run to use one font or `bold=true`.
