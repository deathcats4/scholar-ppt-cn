# Editable object structure

Use this reference for compound page objects and arrows that should stay attached to nodes. An object name or nearby placement does not create a group or connection.

## Build for the intended edit

- Group a numbered circle with its number, and a label container with its text, when they should move together. Keep independent scientific images replaceable. Do not group an entire slide just to satisfy a structure check.
- Bind arrows to nodes when they represent a connection that should follow a moved node. A free-standing reading-direction arrow need not be attached to an unrelated object.
- Assign stable, unique object names. With PptxGenJS, use `objectName`; generate members of each intended group consecutively in the same parent, preserving the intended stacking order.
- Prefer the writer's native grouping and connector APIs when available. Otherwise use the bounded OOXML helper below after writing the PPTX and before final rendering and QA.

## Structure helper

Run:

```powershell
python scripts/structure_pptx.py input.pptx --plan structure-plan.json --output structured.pptx --report structure-report.json
```

The Python API is `structure_pptx(input_path, plan_dict, output_path)`, returning a report. Input and output must be different paths. Example plan:

```json
{
  "groups": [
    {"slide": 1, "name": "GROUP_step_1", "members": ["NODE_step_1", "TEXT_step_1"]},
    {"slide": 1, "name": "GROUP_step_2", "members": ["NODE_step_2", "TEXT_step_2"]}
  ],
  "connectors": [
    {
      "slide": 1,
      "name": "ARROW_step_1_to_2",
      "from": {"shape": "NODE_step_1", "site": 6},
      "to": {"shape": "NODE_step_2", "site": 2}
    }
  ]
}
```

Slides are numbered from 1; names must resolve exactly and uniquely on the specified slide. `site` is the shape's native OOXML connection-site index. The example uses the right and left sites of unrotated ellipses, verified in PowerPoint. Do not assume these indices apply to other shapes or rotations.

The helper supports consecutive top-level members with simple, unrotated transforms, retaining member IDs, geometry, and stacking order. It can bind a supported straight line to named shapes, including members of groups created by the plan. It rejects self-connections, ordinary lines carrying text or shape-only properties, and XML that rebinds one namespace prefix to multiple URIs. Unsupported, ambiguous, or invalid plans fail before writing the output. Do not reorder unrelated objects to force a group; use the source writer for structures outside this scope.

The helper preserves stored connector geometry, but PowerPoint may recalculate an attached line to meet its nodes. If the reference has deliberate gaps between arrows and nodes, inspect this change and make a considered choice about movement behavior and visual fidelity.

## Verify the result

1. Inspect the saved package for real groups and native start/end connection references; confirm text and preserved image bytes have not changed unintentionally.
2. Render the processed file and compare it with the reference and pre-processing preview, particularly line endpoints, text wrapping, stacking, and image crops.
3. In a separate copy, move a representative compound node in PowerPoint or the target application. Check that its text follows and attached arrows remain connected. Report XML inspection separately if application behavior cannot be tested.
4. Run final PPTX QA against the processed file and bind the report to its final hash. Any later save or repair requires renewed rendering and QA.

Do not describe a static XML check as proof of interactive behavior, or describe a replaceable raster figure as editable internal data.
