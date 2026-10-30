# Cross-model drift: M1 vs M2

Each row compares the records M2 shares with M1. Nothing is reconciled; this report only lists differences.

| Section | M1 records | M2 records | Only in M1 | Only in M2 | Content differs | Sequence differs only |
|---|---|---|---|---|---|---|
| BaseInformation | 7 | 7 | 0 | 0 | 1 | 0 |
| Terms | 975 | 733 | 242 | 0 | 0 | 0 |
| Labels | 1349 | 1031 | 318 | 0 | 0 | 0 |
| References | 2629 | 2229 | 402 | 0 | 0 | 2216 |
| Structures | 66 | 55 | 11 | 0 | 0 | 54 |
| Associations | 1394 | 1061 | 333 | 0 | 0 | 37 |
| Rules-Consistency | 3 | 3 | 0 | 0 | 0 | 0 |
| Rules-RollForward | 2 | 2 | 0 | 0 | 0 | 2 |
| Rules-Derivation | 4 | 4 | 0 | 0 | 0 | 4 |
| Rules-Nonstandard | 489 | 212 | 277 | 0 | 0 | 211 |

## BaseInformation: records whose content differs

- `('Local', 'regca')`: TaxonomyDescription
