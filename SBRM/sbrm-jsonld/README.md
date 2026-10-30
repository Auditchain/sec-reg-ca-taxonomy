# Reg CA models in SBRM JSON-LD

These files express two Regulation Crypto Assets base-information models in the OMG *Standard Business Report Model* ([SBRM 1.0 beta 1](https://www.omg.org/spec/SBRM), dtc/25-04-01), as JSON-LD. They are built to the specification *Regulation Crypto Assets in the Standard Business Report Model* (version 2.0), which also gives the conformance evidence and the testing data in `validation/`.

| File | What it is |
|---|---|
| `complete-2026-10-18/regca-complete.definition.jsonld` | SBRM **report definition** for the complete Reg CA framework (all seven forms, 66 fragments, 975 elements, 498 rules) |
| `form-1-crypto-second-offering/regca-1-crypto.definition.jsonld` | SBRM **report definition** for Form 1-CRYPTO (55 fragments, 733 elements, 221 rules) |
| `form-1-crypto-second-offering/regca-1-crypto.report.jsonld` | SBRM **report submission**: the Form 1-CRYPTO demonstration filing (1,169 facts in 47 fact sets) |
| `*/*.shapes.ttl` | **SHACL shapes** generated from each definition's numeric patterns, one SPARQL-based shape per roll-up, roll-forward and arithmetic expression (SBRM §7.3). M1 has 22 and Form 1-CRYPTO has 21. |
| `xbrl/complete-2026-10-18/` | **XBRL taxonomy generated from the complete-model SBRM definition**: `report.xsd`, plus definition, Calc 1.1, label and formula linkbases (975 elements; all 489 XBRL Formula rules, verbatim) |
| `xbrl/form-1-crypto-second-offering/` | **XBRL taxonomy and instance generated from the Form 1-CRYPTO SBRM outputs**: the same set of files (212 formula rules), plus `instance.xml` (1,169 facts, 193 contexts) |
| `lucasuite/regca-complete.json`, `lucasuite/regca-1-crypto.json` | **The files to import into LucaSuite**: each model in LucaSuite's base-information JSON, rebuilt from its JSON-LD (see *Importing into LucaSuite*) |
| `vocab/sbrm-mm-bridge.jsonld` (+ `.ttl`) | Terms for SBRM metamodel elements that the SBRM OWL ontologies do not define, each citing its `xmi:id` in the published `metamodel.xmi` |
| `vocab/xbrl-bridge.jsonld` (+ `.ttl`) | XBRL-specific carry-through terms, kept so the conversion is lossless |
| `context/sbrm-regca.context.jsonld` | The JSON-LD context. Every output also includes it inline, so each file stands alone. |
| `validation/` | The testing data: machine-readable results of every check (`summary.json` gives the overview) |
| `reports/cross-model-drift.md` | Every difference between the two models' shared definitions |
| `observations/SBRM-beta1-observations.md` | Issues found in SBRM 1.0 beta 1 while building this |

The OMG files the build validates against (the four SBRM ontologies, `metamodel.xmi` and the OMG Commons ontologies) and the SPAR ontologies are not copied here. They are published at <https://www.omg.org/spec/SBRM/machine-readable>, <https://www.omg.org/spec/Commons> and <http://www.sparontologies.net/>. `validation/vocabulary-closure.json` records the SHA-256 of each file used.

## Importing into LucaSuite

LucaSuite cannot import JSON-LD yet. Its import takes `.json`, `.xlsx` and `.zip` files only, and rejects anything else as "Unsupported file type". So the build also writes each model in the base-information JSON that LucaSuite imports, rebuilt from the JSON-LD:

| Upload | Model |
|---|---|
| `lucasuite/regca-complete.json` | The complete Reg CA model (definitions only) |
| `lucasuite/regca-1-crypto.json` | The Form 1-CRYPTO model and its demonstration filing (1,169 facts) |

Each file is rebuilt from Layer A alone, and is byte-identical to the base model it came from. LucaSuite therefore receives exactly the base information, with nothing lost or added.

To import a file:
1. In LucaSuite, create a new, empty report, and open it.
2. Open **Load data from Excel or JSON**, and choose the file.
3. Leave **Keep the original ReportingEntityAspect name from the import** ticked. Unticked, LucaSuite replaces the entity on every fact (`PacioliLabsInc | 5067001J8OL3RK15TE82`) with the report's own. Only the super-admin, moderator, enterprise and enterprise operator roles see this box. For other users it is not shown, and LucaSuite replaces the entity.
4. Click **Send data**.

Through the API, send the file as the multipart field `import` to `POST /api/import/{report id}`, with a Sanctum bearer token. The API keeps the file's entity unless `importEntity` is set to something other than 1.

**Checked before upload.** The build replays LucaSuite's importer on both files, using the rules in the LucaSuite source (`validation/lucasuite-preflight.json`):
- **File type:** both are accepted.
- **Model validator:** it passes, including a fetch of each of the six imported XBRL schemas. All six return HTTP 200 with the namespace the model declares.
- **What LucaSuite would store:** every row of both files, with nothing skipped or merged.
- **Controls:** 11 deliberately broken copies are each reported. The first is the JSON-LD itself.

One change LucaSuite makes on import loses nothing here. It stores the `Facts-Dimensions` rows on their facts and drops their `Sequence` column, which in these files is just the row number.

## How to read an output file

Each file holds two named graphs:
- **Layer A** (`…/layer-a`) is lossless. Every record of the base model becomes one SBRM node, and the original JSON file can be rebuilt from Layer A byte for byte.
- **Layer B** (`…/layer-b`) is the SBRM view derived from Layer A:
  - labels and references attached to elements;
  - hypercube line items and dimensions;
  - enumeration value domains;
  - one concept arrangement pattern per fragment (Set, Roll Up, Roll Forward, Arithmetic Expression or TextBlock);
  - the report definition node;
  - for the filing, the report node and its fact sets.

Following SBRM's Financial Report Design Approach (§7.3), every concept is an OWL class, and each fact is an instance of its concept class:

```json
{ "@id": "regca-1crypto:fact/FACTc1a8039789", "@type": "regca:Assets",
  "sbrm-rev:isReportedBy": "regca-1crypto:party/5067001J8OL3RK15TE82/role",
  "cmns-dt:hasTime": "regca-1crypto:period/2027-06-30",
  "sbrm-rst:hasFactValue": { "@type": "sbrm-frst:MonetaryFactValue",
    "cmns-qtu:hasNumericValue": { "@value": "1410000", "@type": "xsd:decimal" },
    "cmns-qtu:hasMeasurementUnit": "iso4217:USD", "xbrlb:decimals": "INF" } }
```

## Where the JSON keys come from

Every key is a compact IRI naming its vocabulary. Each term is taken from the first source in this list that has it:
1. the SBRM ontologies (`sbrm-rev:`, `sbrm-rst:`, `sbrm-frst:`);
2. the OMG Commons ontologies that SBRM imports (`cmns-*:`);
3. the SBRM metamodel, through the bridge vocabulary (`sbrm-mm:`);
4. W3C vocabularies;
5. XBRL carry-through (`xbrlb:`), used only for fields with no SBRM meaning.

No term is minted in an `omg.org` namespace. The `sbrm-mm:` and `xbrlb:` namespaces are hosted under `accounting.auditchain.finance` as a proposal. The full inventory of keys and classes used, generated from the files, is at the end of this README.

## Validation results (latest build)

| Check | Result |
|---|---|
| Round trip (rebuild each input from Layer A) | **Byte-exact** for both models: 5,660,955 and 4,476,837 bytes |
| Layer B regenerated from the rebuilt input | Identical |
| JSON-LD processing (rdflib and pyld) | Both parse every file and agree on the quad counts: 67,665 / 52,842 / 14,293 |
| Vocabulary closure | Every property and class is declared in the pinned SBRM, Commons or SPAR files, the bridge vocabularies, or the model itself |
| Bridge provenance | All 56 cited `xmi:id`s resolve in `metamodel.xmi`; no bridge term duplicates an ontology term |
| Filing structure (1,169 facts) | 0 errors: period types, value types, units, enumeration domains, dimensional validity, fact-set membership |
| Required elements for Form 1-CRYPTO | 93 of 93 present |
| Roll-ups | 20 pass, 0 fail; 1 not evaluable (the total is reported but none of its items are) |
| Roll-forwards | Cash 2 of 2 and equity 2 of 2 pass; supply not evaluable (supply is reported at one instant only) |
| Consistency and derivation rules | Accounting equation 2 of 2, offering price 1 of 1 and BNP tie-out 3 of 3 pass; the BNP ratios pass where their inputs are reported (4 pass, 0 fail, 8 not applicable) |
| **Post-build Arelle validation** (Arelle 2.47.3, separate processes, on the files on disk) | The XBRL files on disk match a fresh generation from the SBRM outputs. Both taxonomy entry points pass XBRL 2.1, Dimensions, Enumerations 2.0 and the formula-linkbase compile with **0 messages**. So does the instance, which is also checked for Calc 1.1, Unit Type Registry and duplicate facts. For each taxonomy, all 3 control copies are rejected: a broken locator (`xbrl.3.5.4:hrefIdNotFound`), an undeclared formula variable (`xbrlve:unresolvedDependency`) and a missing typed domain (`xbrldte:OutOfDTSSchemaError`). Results are in `validation/arelle-postbuild.json`. |
| All 211 XBRL Formula assertions (Arelle) | **0 failed.** Required-element rules: 93 passed. Executable twins of the declarative rules: 7 passed, 1 not evaluated (supply). Other rules: **91 passed, 19 not evaluated**: conditional rules (price ranges, amendments, supplements, solicitations, incorporation by reference, business-day deadlines, foreign currency) whose facts do not occur in this filing. `REGCA_PARAM_REGISTER` holds parameters only. |
| Arelle negative suite | 7 of 7. Mutated instances produce the expected Calc 1.1 inconsistency, unsatisfied assertions, `enum2ie:InvalidEnumerationValue` and `xbrldie:PrimaryItemDimensionallyInvalidError`. A ratio change inside the model's 0.0001 tolerance correctly fires nothing. |
| Negative suite | All 10 deliberately broken copies are rejected, each naming the rule broken |
| **LucaSuite import** (a replay of LucaSuite's importer, `validation/lucasuite-preflight.json`) | Both `lucasuite/` files are byte-identical to their base models. Both pass LucaSuite's model validator, including the six imported XBRL schemas (HTTP 200, namespaces match). Every row is stored: 7 / 975 / 1,261 / 2,619 / 66 / 1,394 / 498 for the complete model, and 7 / 733 / 1,031 / 2,229 / 55 / 1,061 / 221 plus 1,169 facts, carrying all 1,086 dimension rows, for Form 1-CRYPTO. All 11 broken copies are reported. |
| **LucaSuite models, checked row by row** (`validation/lucasuite-import-verification.json`) | Every stored row of every list in the two LucaSuite models, with every field, matches its source. *SBRM Reg CA Taxonomy* matches `lucasuite/regca-complete.json` as imported, and, after the October 18 changes made in LucaSuite, the complete model of record of October 18. *SBRM SEC Reg CA Form 1-CRYPTO* matches `lucasuite/regca-1-crypto.json`, including all 1,169 facts and their 1,086 dimension rows. |
| **SBRM entry point package** (`validation/sbrm-package-checks.json`, `validation/arelle-sbrm-package.xml`) | The package LucaSuite exported to `SBRM/` has the content of `taxonomy/2026-10-18`: the same 1,011 element definitions, 2,324 label relationships, 2,629 references and 493 assertions. Arelle validates it, loaded from its public entry point, with 0 errors and 0 warnings. |
| SHACL (pyshacl) | The filing **conforms** to all 21 shapes. As a positive control, each shape evaluates exactly the instances the validator above evaluates (20 roll-up totals, 4 roll-forward periods, 10 expression instances), so the conformance is not vacuous. |
| SHACL negative suite | 7 of 7 behave as expected. Each of 6 broken copies fires exactly the expected shapes (for example, equity +1 fires the equity roll-forward and the Equity and Liabilities-and-Equity roll-ups). A ratio change inside the model's own 0.0001 tolerance correctly fires nothing. |
| Determinism | Two builds produce byte-identical files |
| Inputs | Unchanged (SHA-256 checked before and after) |

## How these files were produced

One build converts both models, generates the vocabularies and the SHACL shapes, proves the round trips, runs every check, generates the XBRL, writes the LucaSuite import files and, last, validates every XBRL file with Arelle. It runs conversion twice, to check determinism, and exits non-zero if any check fails. `validation/build-log.txt` is its console output and `validation/summary.json` its record. The build tools are described in the specification and are not part of this folder.

To run the shapes against any data graph with another SHACL engine, load the report and its definition together. The shapes need the definition's typed-axis declarations to compare dimensions.

## Limitations

- The XBRL Formula rules are evaluated by Arelle over XBRL generated from the SBRM outputs, not by the SBRM tools themselves. SHACL shapes cover the numeric patterns only. Nineteen conditional rules were not exercised, because this filing has no facts that trigger them.
- Generating XBRL required two choices the base model does not state: typed-dimension domains are declared `xs:integer` (every value is an integer row key), and the entity identifier scheme is the ISO 17442 LEI scheme.
- Turtle exists for the vocabularies and the SHACL shapes; the large definition and report files are JSON-LD only.
- Topics are not built, because the base models hold no topic information.
- LucaSuite imports the `lucasuite/` JSON files, not the JSON-LD. The import check replays LucaSuite's rules from its source (the 1 June 2026 snapshot) and does not run LucaSuite itself. A LucaSuite release that changes those rules needs the check updated.
- `regca:` and model IRIs are identifiers and do not dereference.
- `complete-2026-10-18/` is built from the complete model of October 17, 2026. The October 18 changes were made later, in LucaSuite: 88 documentation labels added and 29 extended, ten references added, and corrections to eight rules. They are in the LucaSuite model *SBRM Reg CA Taxonomy* and in the entry point package in `SBRM/`, but not in `complete-2026-10-18/`. The Form 1-CRYPTO files are built from the model of record of October 18, so they include the changes that concern Form 1-CRYPTO.
- The two models' shared definitions therefore differ: 29 labels differ, 88 labels and 10 references exist only in the Form 1-CRYPTO model, and 4 rules differ. These are the October 18 changes. Each output reflects its own model. See `reports/cross-model-drift.md`.

## Key inventory

<!-- inventory:begin -->

Generated by `tools/inventory.py` from 3 output files. 138 distinct JSON keys and 429 distinct classes; 0 unattributed.

**JSON keys (properties)**

| Source vocabulary | Term | Uses |
|---|---|---|
| SBRM ontology (OMG, normative) | `sbrm-frst:hasOperator` | 49 |
| SBRM ontology (OMG, normative) | `sbrm-rev:hasReportDate` | 1 |
| SBRM ontology (OMG, normative) | `sbrm-rev:isReportedBy` | 1,170 |
| SBRM ontology (OMG, normative) | `sbrm-rst:hasFactValue` | 1,169 |
| SBRM ontology (OMG, normative) | `sbrm-rst:hasReportElement` | 2 |
| SBRM ontology (OMG, normative) | `sbrm-rst:isClosed` | 82 |
| OMG Commons (imported by SBRM) | `cmns-av:explanatoryNote` | 719 |
| OMG Commons (imported by SBRM) | `cmns-cls:isClassifiedBy` | 2 |
| OMG Commons (imported by SBRM) | `cmns-col:compliesWith` | 47 |
| OMG Commons (imported by SBRM) | `cmns-col:hasMember` | 307 |
| OMG Commons (imported by SBRM) | `cmns-cxtdsg:appliesTo` | 10 |
| OMG Commons (imported by SBRM) | `cmns-doc:refersTo` | 4,848 |
| OMG Commons (imported by SBRM) | `cmns-docc:hasTextualContent` | 4,848 |
| OMG Commons (imported by SBRM) | `cmns-dsg:isDefinedIn` | 1 |
| OMG Commons (imported by SBRM) | `cmns-dt:hasDatePeriod` | 162 |
| OMG Commons (imported by SBRM) | `cmns-dt:hasDateValue` | 6 |
| OMG Commons (imported by SBRM) | `cmns-dt:hasEndDate` | 2 |
| OMG Commons (imported by SBRM) | `cmns-dt:hasStartDate` | 2 |
| OMG Commons (imported by SBRM) | `cmns-dt:hasTime` | 1,007 |
| OMG Commons (imported by SBRM) | `cmns-qtu:describesActualExpression` | 727 |
| OMG Commons (imported by SBRM) | `cmns-qtu:hasExpression` | 719 |
| OMG Commons (imported by SBRM) | `cmns-qtu:hasMeasurementUnit` | 284 |
| OMG Commons (imported by SBRM) | `cmns-qtu:hasNumericValue` | 284 |
| OMG Commons (imported by SBRM) | `cmns-rlcmp:isPlayedBy` | 1 |
| OMG Commons (imported by SBRM) | `cmns-txt:hasTextValue` | 509 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:asNestedExpression` | 12 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:asNumber` | 40 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasBeginningBalance` | 6 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasChange` | 6 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasConcept` | 4 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasConceptArrangementPattern` | 121 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasDataType` | 1,013 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasDimension` | 78 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasEndingBalance` | 6 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasFactSet` | 1 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasFragment` | 2 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasInput` | 23 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasLineItems` | 82 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasMemberArrangementPattern` | 76 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasNumber` | 88 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasOperand` | 26 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasPart` | 182 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasPartElement` | 2,455 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasReportLevelRule` | 2 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasTotal` | 23 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:hasValueType` | 1,013 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:id` | 22 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:isAdded` | 88 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:memberElement` | 1,011 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:sequence` | 10,459 |
| W3C / DCMI | `dct:bibliographicCitation` | 4,848 |
| W3C / DCMI | `dct:conformsTo` | 701 |
| W3C / DCMI | `dct:date` | 4,848 |
| W3C / DCMI | `dct:description` | 2 |
| W3C / DCMI | `dct:identifier` | 1,889 |
| W3C / DCMI | `dct:language` | 14 |
| W3C / DCMI | `dct:publisher` | 4,848 |
| W3C / DCMI | `dct:source` | 1,704 |
| W3C / DCMI | `dct:title` | 4,848 |
| W3C / DCMI | `dct:type` | 4,848 |
| W3C / DCMI | `owl:imports` | 2 |
| W3C / DCMI | `prov:wasDerivedFrom` | 49 |
| W3C / DCMI | `rdf:value` | 2,668 |
| W3C / DCMI | `rdfs:label` | 1,887 |
| W3C / DCMI | `rdfs:subClassOf` | 1,013 |
| W3C / DCMI | `skos:definition` | 572 |
| XBRL 2.1 | `xbrl-role:periodEndLabel` | 6 |
| XBRL 2.1 | `xbrl-role:periodStartLabel` | 6 |
| XBRL bridge (carry-through) | `xbrlb:aspectFilter` | 4 |
| XBRL bridge (carry-through) | `xbrlb:associationRole` | 2,455 |
| XBRL bridge (carry-through) | `xbrlb:basedOnSourceFact` | 8 |
| XBRL bridge (carry-through) | `xbrlb:calculationArcrole` | 74 |
| XBRL bridge (carry-through) | `xbrlb:calculationPolarity` | 74 |
| XBRL bridge (carry-through) | `xbrlb:calculationSpecification` | 74 |
| XBRL bridge (carry-through) | `xbrlb:calculationWeight` | 74 |
| XBRL bridge (carry-through) | `xbrlb:calendarPeriodAspect` | 6 |
| XBRL bridge (carry-through) | `xbrlb:closed` | 82 |
| XBRL bridge (carry-through) | `xbrlb:code` | 14 |
| XBRL bridge (carry-through) | `xbrlb:conceptAspect` | 10 |
| XBRL bridge (carry-through) | `xbrlb:contextElement` | 164 |
| XBRL bridge (carry-through) | `xbrlb:decimals` | 284 |
| XBRL bridge (carry-through) | `xbrlb:derivedFact` | 8 |
| XBRL bridge (carry-through) | `xbrlb:dimensionOrder` | 140 |
| XBRL bridge (carry-through) | `xbrlb:enumerationDomain` | 65 |
| XBRL bridge (carry-through) | `xbrlb:extendedLinkRole` | 121 |
| XBRL bridge (carry-through) | `xbrlb:extendedLinkRoleSchemaLocation` | 121 |
| XBRL bridge (carry-through) | `xbrlb:fieldOrder` | 118 |
| XBRL bridge (carry-through) | `xbrlb:fromElement` | 2,455 |
| XBRL bridge (carry-through) | `xbrlb:hasExecutableForm` | 14 |
| XBRL bridge (carry-through) | `xbrlb:headUsable` | 65 |
| XBRL bridge (carry-through) | `xbrlb:identifierScheme` | 1 |
| XBRL bridge (carry-through) | `xbrlb:importsTaxonomy` | 2 |
| XBRL bridge (carry-through) | `xbrlb:jsonLexical` | 3 |
| XBRL bridge (carry-through) | `xbrlb:jsonValueKind` | 20 |
| XBRL bridge (carry-through) | `xbrlb:labelOf` | 2,292 |
| XBRL bridge (carry-through) | `xbrlb:labelRole` | 2,292 |
| XBRL bridge (carry-through) | `xbrlb:namespaceIdentifier` | 14 |
| XBRL bridge (carry-through) | `xbrlb:namespacePrefix` | 14 |
| XBRL bridge (carry-through) | `xbrlb:precondition` | 8 |
| XBRL bridge (carry-through) | `xbrlb:preferredLabelRole` | 12 |
| XBRL bridge (carry-through) | `xbrlb:referenceOf` | 4,848 |
| XBRL bridge (carry-through) | `xbrlb:reportingEntityAspect` | 1 |
| XBRL bridge (carry-through) | `xbrlb:ruleType` | 719 |
| XBRL bridge (carry-through) | `xbrlb:schemaLocation` | 14 |
| XBRL bridge (carry-through) | `xbrlb:sectionName` | 22 |
| XBRL bridge (carry-through) | `xbrlb:sections` | 2 |
| XBRL bridge (carry-through) | `xbrlb:sourceFile` | 2 |
| XBRL bridge (carry-through) | `xbrlb:sourceIndex` | 13,326 |
| XBRL bridge (carry-through) | `xbrlb:sourceSha256` | 2 |
| XBRL bridge (carry-through) | `xbrlb:structureIdentifier` | 121 |
| XBRL bridge (carry-through) | `xbrlb:structureType` | 2,455 |
| XBRL bridge (carry-through) | `xbrlb:typedDomainRef` | 68 |
| XBRL bridge (carry-through) | `xbrlb:unitToken` | 2 |
| Reg CA model (typed axes declared in the definition) | `(any typed-axis property, e.g. `regca:BlockchainNetworkIdentifierTypedAxis`)` | 1,086 |

**Classes (`@type` values)**

| Source vocabulary | Term | Uses |
|---|---|---|
| SBRM ontology (OMG, normative) | `sbrm-frst:Currency` | 1 |
| SBRM ontology (OMG, normative) | `sbrm-frst:LineItems` | 82 |
| SBRM ontology (OMG, normative) | `sbrm-frst:MonetaryFactValue` | 135 |
| SBRM ontology (OMG, normative) | `sbrm-frst:NonNumericFactValue` | 885 |
| SBRM ontology (OMG, normative) | `sbrm-frst:RollForward` | 6 |
| SBRM ontology (OMG, normative) | `sbrm-frst:RollUp` | 23 |
| SBRM ontology (OMG, normative) | `sbrm-rev:Report` | 1 |
| SBRM ontology (OMG, normative) | `sbrm-rev:ReportingParty` | 1 |
| SBRM ontology (OMG, normative) | `sbrm-rst:Dimension` | 68 |
| SBRM ontology (OMG, normative) | `sbrm-rst:FactSet` | 47 |
| SBRM ontology (OMG, normative) | `sbrm-rst:Hypercube` | 82 |
| SBRM ontology (OMG, normative) | `sbrm-rst:Network` | 121 |
| SBRM ontology (OMG, normative) | `sbrm-rst:NumericFactValue` | 149 |
| SBRM ontology (OMG, normative) | `sbrm-rst:ReportDefinition` | 2 |
| SBRM ontology (OMG, normative) | `sbrm-rst:ValueDomain` | 61 |
| OMG Commons (imported by SBRM) | `cmns-doc:Reference` | 4,848 |
| OMG Commons (imported by SBRM) | `cmns-dt:ExplicitDate` | 6 |
| OMG Commons (imported by SBRM) | `cmns-dt:ExplicitDatePeriod` | 2 |
| OMG Commons (imported by SBRM) | `cmns-pts:Party` | 1 |
| OMG Commons (imported by SBRM) | `cmns-qtu:Expression` | 727 |
| OMG Commons (imported by SBRM) | `cmns-qtu:MeasurementUnit` | 1 |
| SPAR DoCO (imported by SBRM) | `doco:Section` | 158 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:AnyURI` | 2 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:ArithmeticExpression` | 26 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:ConsistencyRule` | 8 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:DerivationRule` | 16 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:DisclosureRule` | 410 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:Fragment` | 121 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:Member` | 244 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:MemberMAP` | 76 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:Monetary` | 2 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:NonNumericDataType` | 4 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:Operand` | 52 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:Percent` | 2 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:ReportLevelRule` | 277 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:RollForwardChange` | 14 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:RollForwardRule` | 8 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:RollUpInput` | 74 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:Set` | 117 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:SetMember` | 1,011 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:StructureAssociation` | 2,455 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:Submission` | 1 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:TextBlock` | 6 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:TypedDimension` | 68 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:ValueType` | 1,013 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:XsdBoolean` | 2 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:XsdDecimal` | 2 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:XsdInteger` | 2 |
| SBRM metamodel bridge (metamodel.xmi) | `sbrm-mm:XsdString` | 4 |
| W3C / DCMI | `dct:Agent` | 24 |
| W3C / DCMI | `owl:Class` | 1,013 |
| W3C / DCMI | `owl:DatatypeProperty` | 68 |
| W3C / DCMI | `owl:Ontology` | 2 |
| W3C / DCMI | `rdf:XMLLiteral` | 701 |
| W3C / DCMI | `xsd:anyURI` | 36 |
| W3C / DCMI | `xsd:boolean` | 190 |
| W3C / DCMI | `xsd:date` | 4,889 |
| W3C / DCMI | `xsd:decimal` | 358 |
| XBRL bridge (carry-through) | `xbrlb:DerivedLayer` | 3 |
| XBRL bridge (carry-through) | `xbrlb:ImportedTaxonomy` | 12 |
| XBRL bridge (carry-through) | `xbrlb:Label` | 2,292 |
| XBRL bridge (carry-through) | `xbrlb:LosslessLayer` | 3 |
| Reg CA model (typed axes declared in the definition) | `(any Reg CA concept class, e.g. `regca:Assets`)` | 1,169 |

<!-- inventory:end -->
