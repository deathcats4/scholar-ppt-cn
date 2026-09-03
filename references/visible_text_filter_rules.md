# Visible Text Filter Rules

## Internal workflow language

Do not place internal workflow language into final slides or image-model mockups.

Avoid visible slide text such as:
- template DNA;
- minimal brief;
- archetype;
- inheritance map;
- mockup-derived;
- production planning table;
- production note;
- speaker note;
- this slide is for;
- design suggestion;
- QA note;
- page task;
- source gap;
- internal route;
- internal file or workflow label;
- system prompt or prompt instructions;
- family ID or variant ID;
- placeholder or example-text instructions.

If an internal idea must appear, rewrite it as normal presentation content supported by the source material.

Do not classify a standalone domain term as workflow leakage when it is genuinely
part of the presentation subject. Terms such as `prompt`, `提示词`, `archetype`,
`reading order`, and `阅读顺序` are allowed in an academic slide about language
models, communication, design research, or another source-supported topic. This
does not allow actual internal route names, Template DNA, production planning
tables, family/variant IDs, or implementation instructions to become slide content.

## Slide-production commentary

Final slides should explain the source content, not how the slide was assembled.
Keep figure-selection, cropping, layout, and design decisions in internal planning,
speaker notes, or the QA note unless the user explicitly requests a visible methods
disclosure.

Remove production-facing commentary such as:

- “图件处理：原图完整保留”;
- “局部图经裁切用于突出关键结构”;
- “封面下方使用某图作为全稿视觉线索”;
- “制作说明：本页采用左右布局”;
- `figure handling: preserved as supplied`;
- `design note: used as the visual anchor`.

Normal evidence captions remain allowed. Prefer text such as `Fig. 5a–c 含铁矿物的显微产状`,
`图源：Yue et al. (2022)`, or a direct statement of what the evidence shows. Record
panel selection or mechanical cropping in speaker notes or QA documentation rather
than narrating the production decision on the slide.

## Literature-report presentation labels

For literature reports and journal-club decks, do not use these labels merely to frame normal content:
- 读图要点;
- 读图结论;
- 关键认识;
- 综合判断;
- 支持证据;
- 注意事项;
- 证据观察;
- 预期输出;
- 本文切口;
- 证据页 1/2 or 2/2;
- 基于论文证据的结构化归纳;
- 作者解释;
- 作者综合模型;
- 证据锚点;
- 本页重点;
- 一句话结论.

“核心问题” and “结论” are allowed. Preserve the actual supported statement and remove the editorial label.

Use “提示：” or “注意：” only for genuine warnings required by the source or user. Write all other content as direct academic statements.

## Model self-reference and placeholders

Do not expose model or generation language such as:
- 作为 AI / 作为一个语言模型;
- 根据你的要求;
- 以下是为你生成的;
- 我将为你;
- TODO / TBD;
- lorem ipsum;
- 示例文本;
- 在此插入图片;
- 点击添加标题 / 点击添加文本.

## Source-deck provenance

Do not show internal provenance about template handling in the final presentation. Remove visible text such as `视觉底稿`, `source deck`, `user-supplied reference PPT`, `reference PPT for visual style`, or similar statements that merely document which PPTX supplied the visual system.

Do not place a repeated full `[Sources]` bibliography block in visible slide text as an implementation trace. Speaker notes may retain source/provenance blocks. Use concise evidence-facing figure/source notes on the slide only when they help the audience verify the scientific content, or use the citation format explicitly requested by the user.
