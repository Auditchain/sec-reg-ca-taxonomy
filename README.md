# SEC Regulation Crypto Assets (Reg CA) Taxonomy

A draft XBRL taxonomy for the seven forms of the Securities and Exchange Commission's proposed Regulation Crypto Assets (Release Nos. 33-11434; 34-106150; File No. S7-2026-27; 91 FR 54510, Aug. 21, 2026). It was prepared by Auditchain Labs AG for its comment letter on the proposal.

This is not an official taxonomy of the Securities and Exchange Commission, and the Commission has not reviewed or endorsed it.

## Version 2026-10-16

| | |
|---|---|
| Entry point | https://raw.githubusercontent.com/Auditchain/sec-reg-ca-taxonomy/main/taxonomy/2026-10-16/entrypoint.xsd |
| Namespace | `http://luca.pacioli.ai/report` |
| Prefix | `regca` |
| Taxonomy package | [`packages/sec-reg-ca-taxonomy-2026-10-16.zip`](packages/sec-reg-ca-taxonomy-2026-10-16.zip) |

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
| Form TR | Transition report (Rules 200(e), 305(d) and 400(b)) |

## What it contains

- **961 elements, each defined once:**
  - 568 reportable concepts;
  - 35 open-ended (typed) axes, so that a filer can add as many rows as a form calls for ("each risk factor", "each related person", and so on);
  - 64 tables and sections.
- **Proposed elements:** 88 of the concepts are not required by the proposed rule. Their documentation label says "Proposed by Auditchain Labs; not required by the proposed rule."
- **References:** 2,597. Each element carries, as its reference, the verbatim text of the proposed rule or form item that calls for it or, for financial statement elements, of the FASB Accounting Standards Codification.
- **Validation:** 454 validation assertions (XBRL Formula 1.0), with the offering limits and deadlines held as parameters.

The taxonomy loads and validates with no errors in Arelle (XBRL 2.1, Dimensions 1.0, Calculations 1.1, Extensible Enumerations 2.0 and Formula 1.0).

## Files

| File | Content |
|---|---|
| `taxonomy/2026-10-16/entrypoint.xsd` | Entry point |
| `taxonomy/2026-10-16/report.xsd` | Element definitions |
| `taxonomy/2026-10-16/roles.xsd` | Tables and sections (role types) |
| `taxonomy/2026-10-16/report-pre.xml` | Presentation linkbase |
| `taxonomy/2026-10-16/report-def.xml` | Definition (dimensional) linkbase |
| `taxonomy/2026-10-16/report-cal.xml` | Calculation linkbase |
| `taxonomy/2026-10-16/report-lab.xml` | Label linkbase (standard and documentation labels) |
| `taxonomy/2026-10-16/report-ref.xml` | Reference linkbase |
| `taxonomy/2026-10-16/report-for.xml` | Formula linkbase (validation rules) |
| `taxonomy/2026-10-16/META-INF/` | Taxonomy package metadata and catalog |

## Using it

To validate the taxonomy with [Arelle](https://arelle.org):

```
arelleCmdLine --file packages/sec-reg-ca-taxonomy-2026-10-16.zip --packages packages/sec-reg-ca-taxonomy-2026-10-16.zip --validate --formula=validate
```

The taxonomy was built in LucaSuite (Pacioli.ai).

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
