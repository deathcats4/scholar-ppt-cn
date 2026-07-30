# Production Planning Rules

Store planning facts in `project.json` slide records. Generate a readable
Markdown table from JSON.

Each slide record needs:

1. stable slide ID and current page number;
2. slide title;
3. narrative section;
4. communication task;
5. core message;
6. source asset IDs;
7. layout intent or communication behavior;
8. selected family/variant/archetype only when a downstream builder needs it;
9. layout decision reason and adaptable constraints;
10. density;
11. asset handling;
12. risks.

Planning decides what the slide communicates, not the exact visual skeleton.
Prefer semantic layout intent such as:

- evidence-dominant;
- direct comparison;
- overview-to-detail;
- causal or sequential explanation;
- synthesis;
- open question or tension;
- text-led interpretation.

Do not require a visual-reference ID in the initial plan. Retrieve references
after the communication task and source-asset geometry are known. Keep exact
coordinates, column widths, panel counts, and decorative geometry out of the
plan unless a downstream builder explicitly requires them.

Treat selected family, variant, and archetype fields as revisable production
decisions. They must not override the core message, evidence coverage, or
source-asset readability.

For partial revisions, retain the slide ID and update only the affected record.
