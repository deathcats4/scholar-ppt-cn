# scholar-ppt-cn v3.3

A Chinese academic PPT skill for editable deck creation with a restored production planning table and a mockup family + variants stage.

Core idea:

提纲决定讲述顺序；详细版式库决定页面结构；模板 DNA 决定视觉风格；image model 或 Python 负责生成。

User-facing workflow:

1. Generate a production planning table.
2. Use the table to build a mockup family + variants blueprint.
3. Generate visual samples or direct editable PPT from the blueprint.
4. Approve samples when image-model route is used.
5. Expand/reconstruct editable PPTX.
6. Preview, QA, revise.

The planning table is not a rigid old-style outline. It maps each slide to a narrative section, source asset, source-asset geometry, core message, and detailed layout archetype.


v3.3 adds a formal mockup family + variants stage between the production planning table and any generation step. This preserves the stability of visual families while adding variants to reduce monotony.
