# CJK Typography Rules

Use role-based typography.

1. Prefer font roles extracted from the user template.
2. Without a user template, default editable Chinese text to Microsoft YaHei
   and independent editable Latin text to Times New Roman.
3. Do not infer a concrete font family from a visual reference image. Treat its
   pixels as evidence of weight, hierarchy, and typographic character only.
4. Keep title, heading, body, caption, source-note, and emphasis roles distinct.
5. Use bold only where the role or content requires emphasis.
6. Check locally available fonts before construction. If Microsoft YaHei is
   missing, explain the impact and ask whether to install a useful font when
   practical; otherwise use a documented fallback such as:
   - PingFang SC;
   - Source Han Sans SC;
   - Noto Sans CJK SC.
7. Keep mixed-language runs together when splitting them would damage baseline,
   spacing, or editability.
8. Do not modify text baked into source images.

QA for missing fonts, substitution, unreadable sizes, and lost hierarchy. Do not
require every CJK run to be bold.
