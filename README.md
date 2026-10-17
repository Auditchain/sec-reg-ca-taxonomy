# SEC Regulation Crypto Assets (Reg CA) Taxonomy

A draft XBRL taxonomy for the seven forms of the Securities and Exchange Commission's proposed Regulation Crypto Assets (Release Nos. 33-11434; 34-106150; File No. S7-2026-27; 91 FR 54510, Aug. 21, 2026). It was prepared by Auditchain Labs AG for its comment letter on the proposal.

This is not an official taxonomy of the Securities and Exchange Commission, and the Commission has not reviewed or endorsed it.

## Version 2026-10-18

| | |
|---|---|
| Entry point | https://raw.githubusercontent.com/Auditchain/sec-reg-ca-taxonomy/main/taxonomy/2026-10-18/entrypoint.xsd |
| Namespace | `http://luca.pacioli.ai/report` |
| Prefix | `regca` |
| Taxonomy package | [`packages/sec-reg-ca-taxonomy-2026-10-18.zip`](packages/sec-reg-ca-taxonomy-2026-10-18.zip) |

The package follows the XBRL Taxonomy Packages 1.0 specification. Its catalog maps the entry point address above to the files in the package, so it can be used offline.

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

## What it contains

- **975 elements, each defined once:**
  - 575 reportable concepts;
  - 36 open-ended (typed) axes, so that a filer can add as many rows as a form calls for ("each risk factor", "each related person", and so on);
  - 66 tables and sections.
- **Proposed elements:** 95 of the concepts are not required by the proposed rule. Their documentation label says "Proposed by Auditchain Labs; not required by the proposed rule."
- **References:** 2,619. Each element carries, as its reference, the verbatim text of the proposed rule or form item that calls for it or, for financial statement elements, of the FASB Accounting Standards Codification. The filing provenance elements cite the standards they use (RFC 8785, RFC 6962, FIPS 180-4, CAIP-2 and XBRL Taxonomy Packages 1.0).
- **Validation:** 493 validation assertions (XBRL Formula 1.0), with the offering limits and deadlines held as 30 parameters.
- **Filing provenance:** every form carries a merkle root of its facts, the root of the issuer's previous filing and the record of the root on a blockchain network (see below).

The taxonomy loads and validates with no errors in Arelle (XBRL 2.1, Dimensions 1.0, Calculations 1.1, Extensible Enumerations 2.0 and Formula 1.0).

## Filing provenance (proposed)

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
| 3 | Form 1-CRYPTO, Node Offering | Sept. 1, 2027 | `95d9addf816f231df2e0e79d87abc5f578dbe3e6025efdfbf9934d8969c373e2` | [`0xcd233974…b0ea6ff6`](https://etherscan.io/tx/0xcd233974a3c8fb6df9032c8655428260a6d6626ef4c0d992c1ebec05b0ea6ff6) | 26,215,280 |
| 4 | Form 1-SU, annual update | Jan. 28, 2028 | `98ff45141841d9ae1459dce593efb969b5eb60b3a0e4d699efa522b6de02deaa` | [`0xf43687f3…7a9ad856`](https://etherscan.io/tx/0xf43687f3a90cbe38a72215944da124b1ad385eacadbb0df18f1fa4d47a9ad856) | 26,215,287 |
| 5 | Form 1-KC | Mar. 31, 2028 | `2c184ba8308345c5767a74ba892a672d01df9da6a2252e6da6ace8a9f5af1102` | [`0x49542501…f861177c`](https://etherscan.io/tx/0x495425015ebb969618b888226c6adcda1c53e00d6b2f4c653c521f68f861177c) | 26,215,293 |
| 6 | Form 1-CRYPTO, AUDT Offering | Aug. 15, 2028 | `59132383f213570c98a1d39ebea8a76b9070f9d4e8f8f952a3dbd0ea97b951fd` | [`0x502ab740…9076bf71`](https://etherscan.io/tx/0x502ab7404f8a879e2e9b72bd2c7c56c50ae9b3589abb1f7b1a6a58709076bf71) | 26,215,299 |
| 7 | Form 1-SC | Sept. 8, 2028 | `1aebc5b08f6cb311c1aa3f7e35f711c27d47168f4377b550b921a3b21c2af6e1` | [`0x08bb7ef8…da7241e5`](https://etherscan.io/tx/0x08bb7ef879b2b28a345ccfe64d569b71a36a5741047b18b13afdd965da7241e5) | 26,215,305 |
| 8 | Form 1-UC | Dec. 22, 2028 | `67f0956f27c528924a2fc99d9557fed95220187a8d40cd6815c4ae515c013af5` | [`0x91c01254…2daa329a`](https://etherscan.io/tx/0x91c01254a7091c0274f8b4a106d0c45a48c11358955eb165f5da4d792daa329a) | 26,215,311 |
| 9 | Form TR | Dec. 29, 2028 | `f3dcfbcb423b567d76a20b39650e64b14919581c6be6137574135fa749e13099` | [`0x5e85a575…00a3707b`](https://etherscan.io/tx/0x5e85a5755a7acd1c3c09484fd22eef8a501cee8077a8e8c5313c37f800a3707b) | 26,215,317 |

The method hashes every number as the filing writes it. The filings write numbers smaller than 0.0001 with a one-digit exponent (for example `9.1e-7`), as LucaSuite does, so that the root computed from LucaSuite's export of each filing is the anchored root. Filings 3 to 9 were first anchored with roots computed when those numbers had a two-digit exponent (`9.1e-07`); those transactions are superseded:

| # | Sample filing | Superseded transaction | Block |
|---|---|---|---|
| 3 | Form 1-CRYPTO, Node Offering | [`0xaa14c1f3…a2f15aef`](https://etherscan.io/tx/0xaa14c1f34daa55a2b2061d45fdcf163a0c577eca7d782b250546712ba2f15aef) | 26,214,781 |
| 4 | Form 1-SU, annual update | [`0xb1d87273…c89a006a`](https://etherscan.io/tx/0xb1d872735cd7165ed3c0ec5ba2afc2c7070a7dbe875da24ff166dc63c89a006a) | 26,214,792 |
| 5 | Form 1-KC | [`0xf7107af3…456137ab`](https://etherscan.io/tx/0xf7107af33f92b31d305dcba51b80eaecaa42dfe0c27eb51ed1f23794456137ab) | 26,214,798 |
| 6 | Form 1-CRYPTO, AUDT Offering | [`0x4319961b…9a899e91`](https://etherscan.io/tx/0x4319961b7b44d4e3b8658231e7b5c81c335b2f51440fab1088537a899a899e91) | 26,214,804 |
| 7 | Form 1-SC | [`0x62cc3508…bdd208f6`](https://etherscan.io/tx/0x62cc350807201b02830052a03d1b52375e58cffcf83bf73920d3a165bdd208f6) | 26,214,810 |
| 8 | Form 1-UC | [`0x92aa950f…3871b5a6`](https://etherscan.io/tx/0x92aa950fe3eb380a8072468e3b07671e7dabb7c57a64da1131443b983871b5a6) | 26,214,816 |
| 9 | Form TR | [`0x0df4552f…26d2bc0a`](https://etherscan.io/tx/0x0df4552f156cef48963145ceebf4e9af7e2801842cff17bd6dd0d23126d2bc0a) | 26,214,822 |

## Files

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
| `packages/sec-reg-ca-taxonomy-2026-10-18.zip` | The taxonomy package |
| `tools/regca_merkle.py` | Merkle root of a filing, proofs and chain check |
| `tools/merkle-method-v1.md` | Specification of the merkle method, version 1 |

## Using it

To validate the taxonomy with [Arelle](https://arelle.org):

```
arelleCmdLine --file packages/sec-reg-ca-taxonomy-2026-10-18.zip --packages packages/sec-reg-ca-taxonomy-2026-10-18.zip --validate --formula=validate
```

The taxonomy was built in LucaSuite (Pacioli.ai).

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
