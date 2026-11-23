# Experimental artifacts

Subfolders store **real**, date-stamped scan JSON, model answers and evaluation
metrics. The CLI automatically creates its output JSON files. The generic
`.gitignore` excludes local JSON by default to prevent accidental sensitive lab
information; review/sanitize evidence, then force-add specifically approved
submission outputs with `git add -f results/...`. The final notebook must show
actual outputs saved after YOUR lab runs, not canned sample findings.
