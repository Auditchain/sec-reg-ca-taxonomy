# SEC Regulation Crypto Assets (Reg CA) Taxonomy

A draft XBRL taxonomy for the seven forms of the Securities and Exchange Commission's proposed Regulation Crypto Assets (Release Nos. 33-11434; 34-106150; File No. S7-2026-27; 91 FR 54510, Aug. 21, 2026). It was prepared by Auditchain Labs AG for its comment letter on the proposal.

This is not an official taxonomy of the Securities and Exchange Commission, and the Commission has not reviewed or endorsed it.

## Versions

| Version | Entry point | Taxonomy package |
|---|---|---|
| 2026-10-18 (current) | https://raw.githubusercontent.com/Auditchain/sec-reg-ca-taxonomy/main/taxonomy/2026-10-18/entrypoint.xsd | [`packages/sec-reg-ca-taxonomy-2026-10-18.zip`](packages/sec-reg-ca-taxonomy-2026-10-18.zip) |
| 2026-10-16 | https://raw.githubusercontent.com/Auditchain/sec-reg-ca-taxonomy/main/taxonomy/2026-10-16/entrypoint.xsd | [`packages/sec-reg-ca-taxonomy-2026-10-16.zip`](packages/sec-reg-ca-taxonomy-2026-10-16.zip) |

- Version 2026-10-18 adds the filing provenance sections (see below). Nothing else changed: every element, label, reference, table and rule of version 2026-10-16 is in it unchanged.
- Version 2026-10-16 is kept as it was, so that links to it keep working.
- Both versions use the namespace `http://luca.pacioli.ai/report` and the prefix `regca`.
- Each package follows the XBRL Taxonomy Packages 1.0 specification. Its catalog maps the entry point address to the files in the package, so it can be used offline.

## Forms covered

| Form | What it is |
|---|---|
| Form NOR | Notice of reliance on the startup exemption (Rule 200(c)) |
| Form 1-SU | Startup disclosure statement (Rule 200(d)). Proposed by Auditchain Labs as an official form. |
| Form 1-CRYPTO | Offering statement under the fundraising exemption (Subpart C) |
| Form 1-KC | Annual report (Rule 305(a)) |
| Form 1-SC | Semiannual report (Rule 305(a)) |
| Form 1-UC | Current report (Rule 305(a)) |
| Form TR | Transition report (Rules 200(e), 305(c)–(d) and 400(b)) |

## What version 2026-10-18 contains

- **975 elements, each defined once:**
  - 575 reportable concepts;
  - 36 open-ended (typed) axes, so that a filer can add as many rows as a form calls for ("each risk factor", "each related person", and so on);
  - 66 tables and sections.
- **Proposed elements:** 95 of the concepts are not required by the proposed rule. Their documentation label says "Proposed by Auditchain Labs; not required by the proposed rule."
- **References:** 2,619. Each element carries, as its reference, the verbatim text of the proposed rule or form item that calls for it or, for financial statement elements, of the FASB Accounting Standards Codification. The filing provenance elements cite the standards they use (RFC 8785, RFC 6962, FIPS 180-4, CAIP-2 and XBRL Taxonomy Packages 1.0).
- **Validation:** 493 validation assertions (XBRL Formula 1.0), with the offering limits and deadlines held as 30 parameters.

The taxonomy loads and validates with no errors in Arelle (XBRL 2.1, Dimensions 1.0, Calculations 1.1, Extensible Enumerations 2.0 and Formula 1.0).

## Filing provenance (new in version 2026-10-18; proposed)

Two sections on every form, proposed by Auditchain Labs and not required by the proposed rule:

- **Filing provenance:** the merkle root of the filing, the method used to compute it, the merkle root and date of the issuer's previous filing, and the address of the taxonomy entry point the filing uses.
- **Anchors:** one row for each record of the root on a blockchain network: the network (CAIP-2 identifier), the protocol, the transaction, its block number and date, and a link to the transaction.

How it works:

- The root covers every fact in the filing except the root itself, the method and the anchors. A filing cannot contain its own root or the transaction that records it, so these are left out.
- Each filing's root covers the previous filing's root. An issuer's filings therefore form one chain: a change to any fact of an earlier filing breaks every later link.
- **Method, version 1:**
  - Each fact is written as a JSON object with the keys concept, entity, period, dimensions, unit, decimals and value, leaving out keys with no value. Every value is written as text, exactly as the filing records it (numbers as written, not re-formatted).
  - The object is serialized under RFC 8785 (JSON Canonicalization Scheme).
  - Each leaf is SHA-256 of the byte 0x00 followed by that serialization.
  - The leaves are sorted and combined into the Merkle Tree Hash of RFC 6962, section 2.1.
- One fact can be proven to be in a filing with about ten hashes, without the rest of the filing.
- The full specification is [`tools/merkle-method-v1.md`](tools/merkle-method-v1.md).

### Checking a filing

[`tools/regca_merkle.py`](tools/regca_merkle.py) (Python 3, standard library only) works on filings in the LucaSuite JSON format:

```
python3 tools/regca_merkle.py root  <filing.json>                     # recompute the root and compare it with the reported one
python3 tools/regca_merkle.py proof <filing.json> <FactID>            # proof that one fact is in the filing
python3 tools/regca_merkle.py chain <filing1.json> <filing2.json> ... # check a chain of filings (roots and dates), in filing order
```

To check an anchor, open the transaction: its input data is `0x` followed by the root.

### The nine sample filings

Auditchain Labs anchored the roots of its nine sample filings on Ethereum mainnet (`eip155:1`) on October 17, 2026. Each root is the data of one transaction, sent from `0x504ecea1b583ccf5f2d774e734a7dff101cb70e8` to itself, with no ether transferred. The filings are demonstrations prepared for the comment letter: their filing dates are illustrative, so they are later than the dates of the transactions.

| # | Sample filing | Illustrative date | Merkle root | Transaction | Block |
|---|---|---|---|---|---|
| 1 | Form NOR | Mar. 1, 2027 | `d79c82f0b8967af5d32cccea05249e7ba52b56b92cf8772d4e20a6435038e05f` | [`0x719ae6bc…a96ef999`](https://etherscan.io/tx/0x719ae6bcc3b342d2bf1725eba1032f19fed5c624f5c4065dd1ea9c0aa96ef999) | 26,214,762 |
| 2 | Form 1-SU | Mar. 1, 2027 | `3a66bd1fdd039eb56766309a8782d6585b6c02d29e985f6c3b89d6b0e98c4610` | [`0x2c9b1b24…5e59b86e`](https://etherscan.io/tx/0x2c9b1b2429122d3e4c43d85c3b1c6a888962111139f8212fedf3fd335e59b86e) | 26,214,774 |
| 3 | Form 1-CRYPTO, Node Offering | Sept. 1, 2027 | `e63635c4fd05a1c67726cf74943491c7b12069afabe435169f4e47c0db401668` | [`0xaa14c1f3…a2f15aef`](https://etherscan.io/tx/0xaa14c1f34daa55a2b2061d45fdcf163a0c577eca7d782b250546712ba2f15aef) | 26,214,781 |
| 4 | Form 1-SU, annual update | Jan. 28, 2028 | `cc16d8b861e5066558ad269838c77aa0ba6dbf31977ee0d19977d5b2f6c855d5` | [`0xb1d87273…c89a006a`](https://etherscan.io/tx/0xb1d872735cd7165ed3c0ec5ba2afc2c7070a7dbe875da24ff166dc63c89a006a) | 26,214,792 |
| 5 | Form 1-KC | Mar. 31, 2028 | `3225d6c70bfff9552e3c9c983c538ebfbe76153effb11bd8b2b3d93db8358006` | [`0xf7107af3…456137ab`](https://etherscan.io/tx/0xf7107af33f92b31d305dcba51b80eaecaa42dfe0c27eb51ed1f23794456137ab) | 26,214,798 |
| 6 | Form 1-CRYPTO, AUDT Offering | Aug. 15, 2028 | `28390285fd3bfffde6f2bc932ff639674091f31d3ccf0fd55dfe69004e3b354d` | [`0x4319961b…9a899e91`](https://etherscan.io/tx/0x4319961b7b44d4e3b8658231e7b5c81c335b2f51440fab1088537a899a899e91) | 26,214,804 |
| 7 | Form 1-SC | Sept. 8, 2028 | `dba8b00bead12e723bd00a4a1d289f5a8e5ff3d083af10ceace9fc13806b177e` | [`0x62cc3508…bdd208f6`](https://etherscan.io/tx/0x62cc350807201b02830052a03d1b52375e58cffcf83bf73920d3a165bdd208f6) | 26,214,810 |
| 8 | Form 1-UC | Dec. 22, 2028 | `71a37ec458f0145ef67d00f2724c3258f10aea1dce80bac34f9b91dd09d8177e` | [`0x92aa950f…3871b5a6`](https://etherscan.io/tx/0x92aa950fe3eb380a8072468e3b07671e7dabb7c57a64da1131443b983871b5a6) | 26,214,816 |
| 9 | Form TR | Dec. 29, 2028 | `09f02e872c539bf9c130e93b690bbd6c25f37b6e945e526eccfb821329cbd86d` | [`0x0df4552f…26d2bc0a`](https://etherscan.io/tx/0x0df4552f156cef48963145ceebf4e9af7e2801842cff17bd6dd0d23126d2bc0a) | 26,214,822 |

## Files (version 2026-10-18)

| File | Content |
|---|---|
| `taxonomy/2026-10-18/entrypoint.xsd` | Entry point |
| `taxonomy/2026-10-18/report.xsd` | Element definitions |
| `taxonomy/2026-10-18/roles.xsd` | Tables and sections (role types) |
| `taxonomy/2026-10-18/report-pre.xml` | Presentation linkbase |
| `taxonomy/2026-10-18/report-def.xml` | Definition (dimensional) linkbase |
| `taxonomy/2026-10-18/report-cal.xml` | Calculation linkbase |
| `taxonomy/2026-10-18/report-lab.xml` | Label linkbase (standard and documentation labels) |
| `taxonomy/2026-10-18/report-ref.xml` | Reference linkbase |
| `taxonomy/2026-10-18/report-for.xml` | Formula linkbase (validation rules) |
| `taxonomy/2026-10-18/META-INF/` | Taxonomy package metadata and catalog |
| `tools/regca_merkle.py` | Merkle root of a filing, proofs and chain check |
| `tools/merkle-method-v1.md` | Specification of the merkle method, version 1 |

Version 2026-10-16 has the same files under `taxonomy/2026-10-16/`.

## Using it

To validate the taxonomy with [Arelle](https://arelle.org):

```
arelleCmdLine --file packages/sec-reg-ca-taxonomy-2026-10-18.zip --packages packages/sec-reg-ca-taxonomy-2026-10-18.zip --validate --formula=validate
```

The taxonomy was built in LucaSuite (Pacioli.ai).

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
