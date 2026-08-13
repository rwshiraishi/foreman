# Diagrams

The README org chart ships as committed PNGs, not as a ```mermaid block.

GitHub renders Mermaid in the viewer's browser, measuring label text in one font
and drawing it in another. Labels clip, and each browser clips differently —
Safari and Chrome both truncated this diagram, in different places. Pre-rendering
removes the viewer's browser from the loop.

## Changing the diagram

Edit `orgchart.mmd`, then:

```bash
./regen.sh
```

That renders both variants and rewrites `.stamp`. Running `mmdc` by hand skips
the stamp and CI will fail.

## Rules learned the hard way

- **No multi-line edge labels.** A `<br/>` inside an edge label makes mermaid
  mis-measure the background box and clip the text ("retry feedbacl"). Node
  labels are fine multi-line; edge labels must be short and single-line.
- **Don't hardcode node fills.** Light fills glare in dark mode. Let the theme
  supply fills; mark semantics with stroke or dash instead.
- **CI compares hashes, never re-renders.** PNG bytes are not reproducible
  across machines.

## Verifying sync

`.stamp` hashes the source, config, and both PNGs together. To check that the
committed PNGs match the committed source:

```bash
[ "$(cat diagrams/.stamp)" = "$(bash diagrams/stamp.sh)" ] && echo in-sync || echo STALE
```

A CI job can run exactly that comparison. It must never re-render for a byte
comparison — PNG output is not byte-deterministic across machines.
