# Production Path Summary and Confirmation

Use this rule before any new-deck, image-reference reconstruction, approved-mockup expansion, or broad-redesign production action. The goal is to make the intended scope and production path visible before a long-running operation starts, while keeping internal route labels and implementation IDs private.

## Timing

1. Classify the request before any costly production render, image-model call, PPTX write, or broad-redesign mutation. Cheap discovery needed to write the summary (file listing, metadata, text extraction, or a targeted baseline inspection required by revision rules) is allowed; treat it as preparation, not production.
2. For new-deck work, image-reference reconstruction, approved-mockup expansion, and broad redesign, prepare a concise production-path summary before the first production action. Read this file before route-specific production references when the branch is active.
3. Planning-only work and localized or deck-wide mechanical revision stay lightweight. They do not need a separate confirmation stop. If the request expands into broad redesign or production, run the production-path gate at that boundary.
4. Send the summary in a user-visible assistant message before production tools or mutations. If the request leaves a material decision unresolved, show the summary and wait for the user's answer. The waiting turn delivers no template render, image-generation call, PPTX write, or broad-redesign mutation.
5. If the user has already given a clear production instruction and the material decisions are settled, show the summary and continue in the same turn. A clear instruction includes an explicit deliverable and production action such as `直接生成可编辑 PPTX`, `先做样板`, `按确认样板扩展`, or `直接开始`.
6. For a high-cost full-deck or broad-redesign request without that clear authorization, default to waiting after the summary. Do not infer permission to spend a long run from a vague `做完整 PPT` or `继续做一下`.

## What the user sees

Before any branch starts, name the current stage and user-facing path in one short sentence. For new-deck work, approved-mockup expansion, and broad redesign, follow it with the full summary below. Use ordinary Chinese descriptions, not `Route A`, `Route B`, `Route C`, family IDs, variant IDs, or archetype IDs. Include only decisions that affect the work:

- **目标与范围**：new deck, approved-mockup expansion, broad redesign, or a named revision; include the known slide count or scope.
- **材料与证据**：the sources that will drive the narrative and any evidence or resolution risk that changes the plan.
- **模板关系**：continue the editable source deck, imitate a visual reference, use the bundled reference template, or use content-only planning.
- **制作路径**：for example, `先完成规划表`, `先做 1–2 页独立视觉样板`, `从 PPT 图片重建可编辑 PPTX`, `直接生成可编辑 PPTX`, or `整套逐页生成视觉稿，确认后再重建 PPTX`.
- **停点**：the next approval boundary, if one exists. For sample-first or full-slide-visual workflows, state that pilot and full-mockup approvals remain in force; do not imply that production-path confirmation approves slide composition or scientific content.
- **交付物**：planning table, mockups, editable PPTX, rendered previews, QA report, or the subset requested.
- **假设与待确认项**：state conservative assumptions and ask only about material unresolved choices.
- **运行成本提示**：when useful, say that the next step is a long-running or staged operation; do not invent a duration estimate.

Do not put this operational summary into slides, speaker notes, mockups, or QA artifacts. If the user explicitly asks for internal route labels, they may be named in the response, but still explain the path in plain language.

## Response shape

Use this compact shape, adapting the fields to the active branch:

```text
执行路径：<先做规划表 / 先做 1–2 页视觉样板 / 直接生成可编辑 PPTX / 整套逐页生成视觉稿后重建 PPTX / 局部修订>
范围与目标：<页数、对象和交付范围>
材料与证据：<将使用的来源，以及会影响执行的证据风险>
模板关系：<沿用源 PPT / 参考视觉风格 / 使用内置模板 / 内容-only>
下一停点：<样板审批、整套视觉稿审阅、最终 QA，或无额外停点>
交付物：<本阶段实际会交付的文件或结果>
假设与待确认项：<无则写“无”；有实质歧义则列出问题>
```

When no material item is unresolved and the user already authorized the path, end with `我将按以上路径开始。` and continue. When a material item is unresolved or a high-cost run lacks clear authorization, end with a concise request for confirmation and stop before production.

## When a decision is material

Pause for confirmation when one of these choices could change the work substantially:

- the requested deliverable is unclear between planning, mockups, and editable PPTX;
- image-model design versus template-direct construction is unclear;
- a flattened image is being used as a visual reference versus as a complete asset, or the requested editability boundary is unclear;
- an editable source PPTX could be either the visual reference or the deck to continue in place;
- the scope, slide count, outline, or page order is missing or conflicting;
- a strict source-layout/in-place requirement, overwrite choice, or preservation boundary is unclear;
- the user asks for a full-deck or broad redesign but has not authorized a long production run;
- current-turn instructions conflict with an earlier approval or with the supplied files.

Resolve minor choices conservatively and disclose them in the summary. Missing or unreadable evidence is an evidence-handling issue: follow `evidence_asset_rules.md`, request higher resolution, or use a neutral placeholder as applicable rather than turning every asset issue into a route question.

## Decision matrix

| Branch | Production-path summary | Default stop |
| --- | --- | --- |
| Planning-only | State the planning deliverable in the normal response; no separate gate | Continue and deliver the planning artifact |
| Localized or deck-wide mechanical revision | State the requested scope when useful; no separate gate | Continue within the existing change boundary |
| Representative visual samples | Yes, before the pilot | Start the pilot when the sample request is explicit; stop at the existing sample approval |
| Image-reference reconstruction | Yes for a new deck or multi-slide production; a named localized repair stays lightweight | Continue when the image source, editability boundary, and deliverable are clear; stop before production when a material boundary is unresolved |
| Direct full-deck editable PPTX | Yes, before the long production run | Wait when scope, template relationship, deliverable, or authorization is material and unresolved |
| Full-deck per-slide visual design | Yes, before the pilot | Start the pilot when per-slide image-model design is explicit; keep pilot and full-mockup approvals |
| Approved-mockup expansion | Yes, before expansion | Continue when the approved system and scope are clear; otherwise wait |
| Broad redesign | Yes, before production | Wait unless uninterrupted start is explicit and material choices are settled |

The exempt branches may still receive a one-line plan statement; the exemption removes an extra confirmation turn, not ordinary communication.

## Confirmation semantics

- Treat `确认`, `按这个执行`, `开始`, `直接做`, an unambiguous stage-specific `继续`, or an equivalent affirmative reply to the summary as confirmation of the stated scope and path. A bare `继续` is sufficient only when the preceding approved stage is clear; vague wording such as `继续做一下` is not.
- If the user changes a material assumption, update the summary and wait again before production.
- Once the same scope and path are confirmed, do not repeat this gate at every batch or slide. Keep any route-specific approval gates, batch checks, and final QA gates.
- A production-path confirmation authorizes the selected scope and production path only. It does not approve a visual pilot, a scientific interpretation, a source-grounded mechanism diagram, or a final PPTX.

## Conflict resolution

This gate changes the timing of communication, not the route definitions:

- Internal route selection remains automatic; the user receives a plain-language path summary.
- Template handling and production route remain independent decisions.
- Route A still starts with 1–2 representative samples and normally stops for approval.
- Route C still requires pilot approval and full-mockup review unless uninterrupted completion was explicitly authorized.
- Planning-only remains a lightweight deliver-and-stop path.
- Localized and deck-wide mechanical revisions remain outside Routes A, B, and C unless the request expands into broad redesign.
