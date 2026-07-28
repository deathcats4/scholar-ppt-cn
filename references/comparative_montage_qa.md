# Comparative Montage QA

For expanded decks, compare:

- approved mockup overview when samples exist;
- expanded PPT preview overview.

For direct editable generation, inspect full preview montage for:

- title hierarchy consistency;
- header/footer/page-number consistency;
- source-material placement logic;
- caption/source-note consistency;
- color and border consistency;
- density similarity;
- typography compliance;
- repeated skeletons;
- sudden new visual language;
- text overflow or clipping;
- source asset readability;
- narrative preset coverage;
- planning table coverage.

## Efficient inspection sequence

1. Run deterministic static QA across the full PPTX.
2. Inspect one full-deck montage to identify visual anomalies and repeated
   rhythm problems.
3. Open individual slide previews only for issues reported by static QA,
   visible in the montage, or explicitly raised by the user.
4. Fix affected slides and re-render only those slides when the renderer allows
   it.
5. Use one final montage pass to confirm that the fixes did not disrupt the
   visual system.

Do not default to opening every slide individually. If the user has reviewed the
deck and considers it acceptable, stop unless a deterministic blocking error
remains.
