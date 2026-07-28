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
7. selected archetype/family/variant when applicable;
8. layout decision reason;
9. density;
10. asset handling;
11. risks.

Keep the plan concise. Do not prescribe exact coordinates unless a downstream
builder requires them.

For partial revisions, retain the slide ID and update only the affected record.
