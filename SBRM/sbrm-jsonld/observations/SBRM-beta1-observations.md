# Observations on SBRM 1.0 beta 1 (dtc/25-04-01)

These came from building the Reg CA models in SBRM JSON-LD against the specification and its machine-readable files (version 20241101). Each one notes how the build handles it.

| # | Observation | How the build handles it |
|---|---|---|
| A-1 | Table 8-2 (and the Table 8-6 IRIs) give the namespaces as `https://www.omg.org/SBRM/…`, without `/spec/`. The ontology files, and Tables 8-3 and 8-5, use `https://www.omg.org/spec/SBRM/…`. | Use the `/spec/` IRIs from the TTL files. |
| A-2 | Figures 13–16 (Adjustment, Variance, Arithmetic Expression, Hypercube) are blank in dtc/25-04-01. | Use `metamodel.xmi`. |
| A-3 | The ontology's `RollUp` (`hasSumInput`/`hasSumOutput`) and `RollForward` (`hasInitialFact`/`hasIntermediateFact`/`hasEndingFact`) are **instance-level**, ranging over fact values and facts. The metamodel's Roll Up and Roll Forward are **definition-level**, ranging over Numeric Concepts. A report definition cannot be expressed with the ontology terms alone. | Definitions use metamodel properties through the bridge. |
| A-4 | `sbrm-frst:InstantFact` restricts `sbrm-rst:hasFactValue only cmns-dt:TimeInstant`. This looks like it was meant to be `cmns-dt:hasTime only TimeInstant`; as written, it makes every instant fact's value a time instant. | Instant facts use `cmns-dt:hasTime` → `ExplicitDate`. |
| A-5 | `cmns-dt:DatePeriodFact` is declared in the SBRM FinancialReportElements ontology but placed in the Commons namespace. | Used as published. |
| A-6 | The ontology has no terms for Fragment, Topic, Set/SetMember, the CAP-to-fragment link, hypercube line items and dimensions, report fact sets, or Submission/Publication, all of which the metamodel defines. | Bridge vocabulary. |
| A-7 | Annex A's Turtle uses an undefined `sbrm:` prefix and properties not in the ontology (`hasNumericDataValue`, `hasUnit`, `hasPeriod`, `hasReportingEntity`, `hasOutput`). It also uses `xs:` where the normative prefix is `xsd:`. | Annex A names are not used. |
| A-8 | `sbrm-rev:isReportedBy` has the definition "indicates the party that submits something", copied from `isSubmittedBy`. | Noted only. |
| A-9 | Ontology labels differ from the document's names: ReportingEnvelope is labelled "Report Definition Ontology" and FinancialReportElements "Financial Report Structure Ontology". | Noted only. |
| A-10 | Arithmetic Expression has an operator and operands but no result, and the metamodel defines no operator values, so "A = B × C" cannot be expressed. | The bridge defines `Equals`, `Difference`, `Product` and `Quotient` as `sbrm-frst:Operator` individuals. (`Sum` already exists.) |
| A-11 | Figure 17 has no `Date` datatype, only `dateTime` and `duration`. XBRL date items are common. | A Date datatype individual of kind NonNumericDataType. |
| A-12 | The metamodel's Structure Association whole-part has no network scope, so an element shared between networks with different children cannot be represented. | Checked at build time; Reg CA does not hit it. |
| A-13 | XMI typos: "Explict Dimension", "Role Forward Rule", "has metadata defintion entry", "structue", "strtucture", "set-memeber-report-element". | Bridge local names are corrected, and `rdfs:label` keeps the XMI spelling. |
| A-14 | Annex A.3 says "A synonym for stock is duration". It should say flow. | Noted only. |
| A-15 | `sbrm-rst:StructuralElement` has the synonym "concept arrangement pattern", which conflicts with CAP being a Structure subtype in the metamodel. | Noted only. |
| A-16 | `sbrm-frst:hasRounding` has range `xsd:integer`, so it cannot express exact values (XBRL `decimals="INF"`). Every numeric fact in the Form 1-CRYPTO filing is `INF`. | `xbrlb:decimals "INF"`, with no `hasRounding`. |
| A-17 | The metamodel's Fact "has dimension" points to a Dimension, but there is no construct for a typed-dimension value on a fact. | The axis is a property carrying the value (the Annex A pattern). |
| A-18 | The metamodel and ontology have no fact identifier. | `dct:identifier`. |
| A-19 | `sbrm-frst:hasOperator` is used in the `sbrm-frst:RollUp` restriction (`owl:onProperty`) but never declared as a property in `FinancialReportElements.ttl`. | Used as published, and reported by the vocabulary-closure check. |
