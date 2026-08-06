# CJK Typography Rules

## Font Priority

- Follow any font explicitly specified by the user.
- Preserve the font system from a user-provided template when the user asks to continue it.
- Otherwise, default all editable Chinese and mixed CJK/Latin text to `Microsoft YaHei`.
- Whether the current operating system has Microsoft YaHei installed does not change the declared delivery font in the PPTX. If a renderer substitutes the font during preview, disclose the substitution and do not silently rewrite the delivery file to another CJK font.

## Default Sizes

For a 16:9 deck without a user template:

| Role | Default size |
|---|---:|
| Cover title | 32-40 pt |
| Slide title | 28-32 pt, usually about 30 pt |
| Body | Follow template, approved mockup, and rendered readability |
| Defense or large-room body | Prefer larger body text when practical, but do not enforce a universal floor |
| Secondary short label | 16-18 pt |
| Caption | 12-14 pt |
| Source, copyright, page number | 9-11 pt |

These ranges support visual hierarchy. They are not mandatory delivery thresholds. A user template's sizes may be preserved, but visibly tiny body text should be cut, rewritten, or split across slides when it materially hurts readability.

## Body Size Policy

For body font size, match v3.3.1 behavior: do not enforce a universal 16 pt floor, 18-20 pt target, or body-size delivery blocker. Use the user template, approved mockups, slide density, expected projection context, and rendered readability to decide whether body text is acceptable.

- "Effective size" means the final displayed PowerPoint size. If a text box contains `fontScale` or `<a:normAutofit>`, calculate effective size as declared size multiplied by scale when reporting readability concerns.
- Body text using `fit: "shrink"`, `<a:normAutofit>`, or automatic size reduction should be reported for readability review, but it is not a deterministic delivery-blocking error by itself.
- Fixed slide count, fixed layout, preserving full source text, or keeping a column width can still create readability problems; resolve important problems by shortening, expanding, redistributing, or splitting content.

## Do Not Solve Crowding by Shrinking Text

- Do not mechanically shrink body text merely to keep all source text intact.
- When text does not fit, use this order: remove repetition -> shorten sentences -> remove minor labels -> expand the text area -> redistribute content -> split the slide.
- Source-image text is not mechanically judged as editable body text, but it still requires visual review for projection suitability.

## Text Roles and QA Floors

For new PPTX generation, use object-name prefixes where possible:

- `TITLE_`: slide title;
- `BODY_`: body, research judgment, and main explanation;
- `LABEL_`: short label;
- `CAPTION_`: necessary caption;
- `SOURCE_`: source and copyright;
- `PAGE_NUMBER_`: page number.

QA should use object roles first, then fall back to position, text length, and font-size heuristics. Body-size findings are readability review items, not deterministic delivery blockers. Extremely small text can still be reported as a warning for visual inspection.

## Caption Color

- `Fig. 1` / `Table 1` numbers and caption body should default to black or dark gray, such as `#000000` or `#222222`.
- Source, copyright, footer, and supplementary notes may use gray.
- Do not make main captions gray merely because a reference or template uses gray for source notes, unless the user template clearly requires it.

## Weight

- Use bold for cover titles, slide titles, section titles, key conclusions, and genuinely emphasized keywords.
- Use regular weight for body, captions, sources, page numbers, and auxiliary explanations.
- Short headings may be bold, but do not bold the entire body.
- Use the generation tool's native bold property. With PptxGenJS, explicitly set `fontFace: "Microsoft YaHei"` and use `bold: true` only when emphasis is needed.
- Do not simulate bold with outlines, shadows, repeated text, or unrelated fonts.

## Latin and Mixed Text

- Mixed Chinese/Latin text defaults to Microsoft YaHei for stable baselines, wrapping, and editability.
- Pure English paper titles, journal names, or independent English text blocks may use Times New Roman only when there is a design reason.
- Mathematical formulas may use suitable formula fonts or equation objects, while surrounding Chinese explanation remains in Microsoft YaHei.

## Raster Mockup Typography

Image-model mockups do not install or reliably reproduce a named font. A prompt asking for Microsoft YaHei can only request a similar visual character.

- Ask for a restrained modern Chinese sans-serif appearance visually close to Microsoft YaHei.
- Do not claim that a raster mockup actually uses Microsoft YaHei.
- Avoid calligraphic, handwritten, decorative, outlined, shadowed, distorted, or artificially condensed lettering.
- Use raster mockups to judge hierarchy, density, line length, and relative scale, not exact point sizes.
- During editable reconstruction, explicitly set `fontFace: "Microsoft YaHei"` and apply the real typography thresholds in this file.

## Final Check

- Check that titles use the actual bold property.
- Check that body text is not accidentally bolded.
- Check whether body text is visibly too small, clipped, or overcrowded.
- Check whether body `normAutofit` / shrink-to-fit creates visible readability problems.
- Check that Fig./Table captions are black or dark gray by default and visually distinct from source notes.
- Check font substitution, abnormal wrapping, Chinese punctuation, and lost hierarchy.
- Do not modify text already baked into source images.
