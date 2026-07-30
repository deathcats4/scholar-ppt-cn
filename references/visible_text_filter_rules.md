# Visible Text Filter Rules

Final slides speak to the audience, not to the agent building or reviewing the
deck.

## Internal workflow language

Do not expose terms such as:

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
- internal file or workflow label.

## Defensive meta-language

Keep agent-facing epistemic guardrails in `project.json`, QA results, or speaker
notes. Do not place instructions about how the audience or the builder must not
misread the evidence into visible slide copy.

Review and normally rewrite visible phrases such as:

- "注意：这是间接约束";
- "不能把……误写成……";
- "不要将……理解为……";
- "评价原则：区分……";
- "作者优选……，不能视为直接测得……";
- "这篇论文最重要的贡献不是……而是……".

State the supported academic content directly:

- prefer "区域年代学证据将主要成矿阶段收窄至 367–331 Ma" over a
  warning not to misread the interval;
- prefer "矿化发生在容矿火山岩形成之后" over "不能早于";
- prefer "深部靶区有待钻探验证" over an agent-style caution;
- prefer a direct contribution statement over "不是……而是……".

Use neutral evidence verbs such as "显示", "支持", "限定", "指向", "倾向" and
"尚未直接验证". If uncertainty or a limitation is itself the slide's
communication task, present it as an academic finding or limitation, not as an
instruction to the audience.

Do not use red warning treatments merely to protect against possible
over-interpretation. Reserve them for a real anomaly, contradiction, risk, or
critical boundary that the slide is explicitly discussing.

If an internal idea must appear, rewrite it as normal presentation content.
