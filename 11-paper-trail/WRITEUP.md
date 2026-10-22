# Paper Trail

OSINT · 300 points · 5 solves

Flag: `CLUB{m3tadata_n3v3r_sl33ps}`

> Northwind Labs sent out this memo after "redacting" a sensitive token. Whoever did the redacting wasn't very careful. Find out what the memo said before it was cleaned up.

`report.pdf` is a one-page memo that looks harmless when opened:

```
NORTHWIND LABS - INTERNAL MEMO - FINAL
Subject: Q3 infrastructure review
...
Recovery token: [REDACTED]
```

A PDF can be saved incrementally: instead of rewriting the file, the editor appends the changes to the end and leaves the original bytes in place. An incrementally saved PDF can still contain every earlier version.

## Finding the earlier version

The first hint is "Check the file's metadata. Does anything mention other versions?"

```
$ pdfinfo report.pdf
Title:    Q3 Infrastructure Review
Subject:  Final - earlier drafts archived
Keywords: final, redacted, infra
Author:   dana.whitfield
```

"Earlier drafts archived" says there's more than one version. Each complete save ends with `%%EOF`, so count them:

```
$ grep -a -c '%%EOF' report.pdf
2
```

Two saves. The second trailer also contains `/Prev 842`, which points back to the previous cross-reference table at byte 842. The second hint covers this: "A PDF can be saved by appending changes. The old content may still be inside."

Cutting the file just after the first `%%EOF` recovers the first version:

```
$ head -c 1057 report.pdf > draft.pdf
```

`draft.pdf` shows the memo before redaction:

```
NORTHWIND LABS - INTERNAL MEMO - DRAFT
...
Recovery token: CLUB{m3tadata_n3v3r_sl33ps}
```

Its metadata is different too. The title is "Q3 infra review DRAFT" and the author is `dwhitfield`, where the final version says `dana.whitfield`.

`solve/pdf_revisions.py` splits the file at every `%%EOF` and prints the text and metadata of each revision. `pdfresurrect` does the same job.

## The decoy

The second revision has a hidden sticky-note annotation, marked invisible, written by `dana.whitfield`:

```
CLUB{redact3d_f0r_a_r3ason}
```

It's in the final version and has the right format, which makes it tempting. But the challenge asks what the memo said before it was cleaned up, and that's the token in the first revision.

## Notes

Placing `[REDACTED]` or a black box over text doesn't remove it. Proper redaction deletes the content and saves a clean file without the old revisions or identifying metadata. When analysing a document, check the metadata and the revision history as well as the visible page.
