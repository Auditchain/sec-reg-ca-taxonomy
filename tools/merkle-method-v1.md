# Reg CA filing merkle tree, version 1

The method behind the element `regca:FilingMerkleRootMethod` and its member `regca:FilingMerkleTreeVersion1Member`. Proposed by Auditchain Labs; not required by the proposed rule.

It gives one 32-byte root for a filing. The root covers every fact of the filing except the root itself, the method and the table of anchors. Anyone can recompute it from the filing and compare it with the root reported in the filing and with the root recorded on a blockchain network.

## Input

A filing in the LucaSuite JSON format: an object whose sections include `BaseInformation`, `Facts` and `Facts-Dimensions`. The other sections (the taxonomy) are not used.

## Steps

1. **Full names.** `BaseInformation` maps each `NamespacePrefix` to its `NamespaceIdentifier`. The full name of a qualified name `p:local` is the namespace identifier of `p`, then `#`, then `local`. For example, `regca:DocumentType` becomes `http://luca.pacioli.ai/report#DocumentType`. If `p` has no namespace in `BaseInformation`, `p` itself stands in for the namespace (`p#local`). A name with no colon is kept as it is.

2. **Facts left out.** The names below are compared as written in the filing, which uses the prefix `regca` for `http://luca.pacioli.ai/report`. A fact is left out if:
   - its `ConceptAspect` is `regca:FilingMerkleRoot` or `regca:FilingMerkleRootMethod`; or
   - it has a `Facts-Dimensions` record (same `FactID`) whose `Dimension` is `regca:FilingAnchorIdentifierTypedAxis`.

3. **One object for each other fact,** with these keys:

   | Key | Value |
   |---|---|
   | `concept` | the full name of `ConceptAspect` |
   | `entity` | `ReportingEntityAspect`, as written (for example `PacioliLabsInc \| 5067001J8OL3RK15TE82`) |
   | `period` | `CalendarPeriodAspect`, as written (`2027-03-01`, or `2027-01-01 \| 2027-12-31` for a duration) |
   | `dimensions` | an object with one entry for each `Facts-Dimensions` record of the fact: the key is the full name of `Dimension`; the value is the full name of `Member` if `Member` is not empty, and otherwise the typed value `Value` as text, a number exactly as written (for example `1`). A fact has at most one record for each dimension, and every record has either a `Member` or a typed `Value`. |
   | `unit` | `Units`, as written |
   | `decimals` | `Rounding`, as written |
   | `value` | `FactValue` as text: a string as it is; a number exactly as written in the filing's JSON text (for example `716666.67` or `9.1e-7`, not re-formatted); `true` or `false` for a boolean. A null value leaves the key out. |

   In this format `ReportingEntityAspect`, `CalendarPeriodAspect`, `Units` and `Rounding` are strings. Every value in the object is therefore a string or, for `dimensions`, an object of strings. No text is trimmed or Unicode-normalized. A top-level key whose value is an empty string, an empty object or null is left out; inside `dimensions`, every record gives an entry.

4. **Serialization.** The object is serialized under RFC 8785 (JSON Canonicalization Scheme): keys sorted by their UTF-16 code units (at both levels), no whitespace, UTF-8, non-ASCII characters written as they are. Because every value is a string, only the RFC 8785 rules for strings apply.

5. **Leaves.** Each leaf is SHA-256 (FIPS 180-4) of the byte `0x00` followed by the serialization: the leaf hash of RFC 6962, section 2.1.

6. **Order.** The leaves are sorted in ascending order of their 32 bytes. Identical leaves are all kept. The order of the facts in the file therefore does not matter.

7. **Root.** The Merkle Tree Hash of RFC 6962, section 2.1, over the sorted leaves:
   - one leaf: the leaf itself;
   - n > 1 leaves: SHA-256 of `0x01`, the root of the first k leaves and the root of the remaining n − k leaves, where k is the largest power of two smaller than n;
   - no leaves: SHA-256 of the empty string.

8. **Format.** The root is written as 64 lowercase hexadecimal characters. On a blockchain network it is recorded as the data of a transaction: `0x` followed by the root.

## Chain

Each filing other than the issuer's first reports, as facts covered by its own root, the root of the issuer's previous filing (`regca:PreviousFilingMerkleRoot`) and that filing's date (`regca:PreviousFilingDate`, equal to the previous filing's `regca:DocumentDate`). The order of the filings is the chain itself: each filing names the root of the one before it. Two filings can share a date. A change to any fact of an earlier filing changes its root, and so breaks every later link.

## Proof of one fact

The audit path of RFC 6962, section 2.1.1, for the fact's leaf in the sorted list proves that the fact is in the filing with about log2(n) hashes, without the rest of the filing. The proof gives, from the leaf up, each sibling hash and whether it sits on the left or the right; with these, the verifier needs neither the leaf's position nor the number of leaves. The proof shows that the fact is covered by the root; it does not prove how many facts the root covers.

## Reference implementation

`tools/regca_merkle.py` (Python 3, standard library only).
