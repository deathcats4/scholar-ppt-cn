# CJK Typography Rules

For decks containing editable Chinese text:

- every editable run containing CJK characters must use Microsoft YaHei / 微软雅黑;
- every editable run containing CJK characters must be set to 加粗 / bold;
- English, numbers, units, and formulas default to Arial when separated into their own runs;
- text inside source images is not modified.

Correct implementation:
- font family = Microsoft YaHei / 微软雅黑;
- bold = true / 加粗开启.

Do not treat "Microsoft YaHei Bold" as a separate font name.
