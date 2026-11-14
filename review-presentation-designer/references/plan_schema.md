# JSON input contract for build_review_deck.py

Root:

```json
{
  "deck_title": "...", "subtitle": "...", "author": "...",
  "mode": "production", "language": "zh", "theme": "editorial-light",
  "disclaimer": "", "slides": [
    {"type":"cover","title":"...","subtitle":"..."},
    {"type":"taxonomy","title":"...","epistemic_status":"AUTHOR-PROPOSED",
     "claim_ids":["C001"],"source_ids":[],"parent":"Top-level frame",
     "items":[{"label":"Role A","body":"Definition","tag":"R1"}],
     "takeaway":"Not an empirical ranking", "speaker_notes":"..."}
  ]
}
```

Every slide needs `type`, `title`; content slides should have `epistemic_status` and `claim_ids`. `source_ids` are source ledger IDs, not loose author-year strings; they appear in the footer and notes. Slides may use `subtitle`, `takeaway`, `speaker_notes`, `comparison_mode`, `caveat`. `mode` is `production` (requires a valid claim ledger to substantiate factual statements) or `demo` (watermark, no implied research evidence).

Slide data:

- `big_idea`: `statement`, `context`, `pillars` list (up to 3).
- `scope`: `columns` three `{heading,body,items}`; optional `takeaway`.
- `taxonomy`: `parent`, `items` 3–4 `{label,body,tag}` and `takeaway`.
- `mechanisms`: `items` 2–3 `{label,role,input_a,input_b,operator,output,note}`.
- `lanes`: `items` 3–4 `{code,label,question,tests,interpretation}`.
- `comparability`: `checks` five strings, `outcomes` 3 `{label,body}`.
- `matrix`: `columns` list (up to 5), `rows` 3–6 list of lists of strings, `takeaway`, `comparison_mode` (`matched`,`conditional`,`unmatched`).
- `evidence_map`: `items` up to 4 `{claim,status,source,limitation}`; `takeaway`.
- `timeline`: `tracks` up to 3 `{label,nodes:[{time,label,note}]}`; dates/years must be sourced in production. Sourced `edges` not automatically rendered; add explicit labeled lines manually only when verified.
- `debate`: `left` and `right` `{heading,body,evidence}`, `resolution`, `takeaway`.
- `agenda`: `items` 3 `{number,heading,method,deliverable}`.
- `synthesis`: `items` 3–4 `{status,title,body}`.
- `figure`: `path`, `caption`, `credit`, `fit` (`contain` default). Picture remains image, caption/text are editable. Missing file is a hard error.
- `closing`: `statement`, `points` (up to 3), `speaker_notes`.

See the executable `examples/demo_review_plan.json`; it is intentionally illustrative, uncited, and visibly stamped DEMO on every slide. For real review content, replace it with a source-backed plan and ledger, not just an edited demo disclaimer.
