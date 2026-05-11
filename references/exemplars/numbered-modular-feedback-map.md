# Numbered modular feedback map · pattern exemplar

## What this exemplar covers

A dense landscape figure pattern for papers whose contribution is best
shown as a **system of interacting modules plus a feedback / control
layer**. Use it when a single left-to-right pipeline would hide the
fact that several evidence sources, state summaries, decisions, and
returned signals interact.

This is a **style-only abstraction** from a user-provided local figure.
Do not copy source labels, notation, domain objects, icon meanings, or
paper-specific semantics.

## Why the pattern works

### Layout: wide modular map with a feedback base

The figure uses a wide canvas with three visual zones:

- a left / centre work area made of several numbered modules,
- a right status or outcome column,
- a bottom strip spanning the canvas for feedback, update, or validity
  control.

This lets the reader see both the forward path and the returning signal
without turning the figure into a vertical stack.

### Numbered badges stabilize dense structure

Small circular badges attached to panel corners (`1.1`, `1.2`, `2`, ...)
give the reviewer an explicit reading order. They also allow related
submodules to share a prefix without forcing all panels into identical
sizes.

### Colored containers carry semantic grouping

Each major concept family gets one border color and a very light matching
background. The fill should stay pale; the border, panel title, arrows,
and key glyph accents do the semantic work. This gives strong grouping
while keeping dense interiors readable.

### Main flow and feedback flow are visually distinct

Use thick solid arrows for the main forward path. Use dashed or routed
arrows for feedback, auxiliary evidence, or returned control signals.
The distinction should be visible before any arrow label is read.

### Small assets express module roles

The style relies on compact glyph assets: dots for instances, bars for
state, mini networks for learned components, queues / rows for system
state, and small charts for returned evidence. These assets should be
semantic thumbnails, not decorative illustrations.

## Patterns worth lifting

- **Asymmetric landscape layout**: dense module cluster on the left /
  centre, status or outcome column on the right, feedback strip below.
- **Corner badges** for staged reading order in a dense multi-panel map.
- **Soft colored containers**: pale fill + stronger colored stroke +
  title in the same semantic color.
- **Solid vs dashed path grammar**: primary forward path vs feedback /
  auxiliary / boundary path.
- **Bottom control strip** when the main contribution is a returned
  constraint, update, audit, or validity layer.
- **Role-specific mini-assets** inside panels, with editable drawio text
  kept outside assets whenever possible.

## Things to be careful with

- Do not use this pattern for a simple sequential method; it will look
  over-engineered.
- The color palette must map to the paper's actual ontology. Avoid
  assigning colors by visual taste alone.
- Badges need a real reading order. If the order is not meaningful, use
  unnumbered section headers instead.
- Keep text short. This pattern tolerates many objects, not many words.
- Never retain the source exemplar's names, variables, tasks, claims, or
  icon meanings. Lift only the layout grammar and visual hierarchy.

## ASCII layout sketch

```
                              <short figure title>

+----------------------------+     +----------------------------+     +------------------------------+
| 1.1  input / evidence      | --> | 1.2  state summary         | --> | 2  status / outcome column   |
|                            |     |                            |     |                              |
| dots, traces, thumbnails   |     | compact bars / rows        |     | repeated rows or entities    |
| grouped input signals      |     | grouped by concept         |     | system-level state           |
+----------------------------+     +----------------------------+     +------------------------------+
              |
              v
+----------------------------+     +----------------------------+
| 1.3  model / interpreter   | --> | 1.4  fusion / decision     | - - - - - - - - - - - - - - ->
|                            |     |                            |        dashed auxiliary path
| small network or lens      |     | mixed signals become one   |
| role-specific glyph        |     | routed output              |
+----------------------------+     +----------------------------+

+--------------------------------------------------------------------------------------------+
| 4  feedback / control / validity strip                                                     |
|                                                                                            |
| returned signal  <--  aggregation  <--  check / constraint  <--  status / outcome          |
+--------------------------------------------------------------------------------------------+
```
