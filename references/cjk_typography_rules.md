# CJK Typography Rules

## Font Priority

- Follow any font explicitly specified by the user.
- Preserve the font system from a user-provided template when the user asks to continue it.
- Otherwise, default all editable Chinese and mixed CJK/Latin text to `Microsoft YaHei`.
- Whether the current operating system has Microsoft YaHei installed does not change the declared delivery font in the PPTX. If a renderer substitutes the font during preview, disclose the substitution and do not silently rewrite the delivery file to another CJK font.

## Font Size Policy

Do not use a fixed point-size table as the authority for reconstructed slides.
When approved image-model mockups or a user template exist, match the visible
hierarchy, density, line length, and relative scale in the rendered reference.
After generating the editable PPTX, render the deck and adjust font sizes until
the slide feels aligned with the approved mockup or template system.

## Body Size Policy

Do not enforce a universal body-size floor, target range, role table, or body-size delivery blocker. Use the user template, approved mockups, slide density, expected projection context, and rendered readability to assess body text.

- Fixed slide count, fixed layout, preserving full source text, or keeping a column width can still create readability problems; resolve important problems by shortening, expanding, redistributing, or splitting content.

## Do Not Solve Crowding by Shrinking Text

- Do not mechanically shrink body text merely to keep all source text intact.
- When text does not fit, use this order: remove repetition -> shorten sentences -> remove minor labels -> expand the text area -> redistribute content -> split the slide.
- Source-image text is not mechanically judged as editable body text, but it still requires visual review for projection suitability.

## Text Roles

For new PPTX generation, use object-name prefixes where possible:

- `TITLE_`: slide title;
- `BODY_`: body, research judgment, and main explanation;
- `LABEL_`: short label;
- `CAPTION_`: necessary caption;
- `SOURCE_`: source and copyright;
- `PAGE_NUMBER_`: page number.

Use text roles to preserve hierarchy and editability. Do not derive static font-size thresholds from role names.

## Caption Color

- `Fig. 1` / `Table 1` numbers and caption body should default to black or dark gray, such as `#000000` or `#222222`.
- Source, copyright, footer, and supplementary notes may use gray.
- Use gray main captions only when the user template requires it.

## Weight

- Select font weights from the user template, Template DNA, approved mockups, content hierarchy, and rendered readability.
- All-bold, regular-weight, and mixed-weight systems are allowed.
- Keep the selected weight system consistent across equivalent text roles.
- Use the generation tool's native weight property. With PptxGenJS, explicitly set `fontFace: "Microsoft YaHei"` and set `bold` according to the selected visual system.
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
- During editable reconstruction, explicitly set `fontFace: "Microsoft YaHei"`, then tune point sizes by rendering and comparing against the approved mockup or template rhythm.

## Final Check

- Check that titles use the intended native weight property.
- Check that rendered font weights match the selected visual system and preserve clear hierarchy.
- Check whether the rendered editable text visually matches the approved mockup or template hierarchy.
- Check whether body text is clipped, overcrowded, or visibly out of scale with the page.
- Check that Fig./Table captions are black or dark gray by default and visually distinct from source notes.
- Check font substitution, abnormal wrapping, Chinese punctuation, and lost hierarchy.
- Do not modify text already baked into source images.
