# Production Planning Table Rules

Create the production planning table before image or PPTX generation. Record the narrative, content, source assets, source-asset geometry, and the layout intent needed by each slide.

Required columns:

1. slide number;
2. slide title;
3. narrative section;
4. communication task;
5. source asset(s);
6. source-asset geometry;
7. core message;
8. layout intent / candidate structure;
9. density level: low / medium / high;
10. asset handling: preserve / overview+detail / split / cross-slide / not-use / request-higher-resolution;
11. notes and risk: fact check, readability, translation, missing asset, etc.

Keep the table concise. The layout-intent field describes the communicative arrangement and its constraints, without exact geometry coordinates or internal IDs. Examples include:

- dominant figure on the left, conclusion rail on the right;
- overview figure with two detail zooms;
- two evidence groups in direct comparison with a synthesis row;
- process stages in sequence with a mechanism explanation zone.

This field is a planning input, not a final composition lock. Do not require a family ID, variant ID, or archetype ID in the production planning table.

After planning, resolve the candidate structure into a mockup family, variant, and (when needed) a detailed fallback archetype using the communication task, evidence relationships, source geometry, density, readability, and deck rhythm. The detailed layout selection belongs to scholar-ppt-cn, not to the reference/template deck.

When a visual reference or template is active, use its Template DNA to style the resolved layout consistently. When editable native assets are available, reuse them inside or around the resolved layout where appropriate.

Do not map scientific content slides to old template/result/discussion/data/microscopy page layouts unless the user explicitly identifies a source page whose layout should be preserved or reused. Stable frame pages such as cover, table of contents, section divider, and closing pages may retain their source structure when appropriate.
