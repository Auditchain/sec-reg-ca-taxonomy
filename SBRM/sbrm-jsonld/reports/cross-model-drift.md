# Cross-model drift: M1 vs M2

Each row compares the records M2 shares with M1. Nothing is reconciled; this report only lists differences.

| Section | M1 records | M2 records | Only in M1 | Only in M2 | Content differs | Sequence differs only |
|---|---|---|---|---|---|---|
| BaseInformation | 7 | 7 | 0 | 0 | 1 | 0 |
| Terms | 975 | 733 | 242 | 0 | 0 | 0 |
| Labels | 1261 | 1031 | 318 | 88 | 29 | 0 |
| References | 2619 | 2229 | 402 | 10 | 0 | 2206 |
| Structures | 66 | 55 | 11 | 0 | 0 | 54 |
| Associations | 1394 | 1061 | 333 | 0 | 0 | 37 |
| Rules-Consistency | 3 | 3 | 0 | 0 | 0 | 0 |
| Rules-RollForward | 2 | 2 | 0 | 0 | 0 | 2 |
| Rules-Derivation | 4 | 4 | 0 | 0 | 0 | 4 |
| Rules-Nonstandard | 489 | 212 | 277 | 0 | 4 | 207 |

## BaseInformation: records whose content differs

- `('Local', 'regca')`: TaxonomyDescription

## Labels: records whose content differs

- `('regca:NetworkNativeTokenSymbol', 'Documentation', 'en')`: Label
- `('regca:EffectiveStakeControlledOnNetwork', 'Documentation', 'en')`: Label
- `('regca:TotalActiveStakeOnNetwork', 'Documentation', 'en')`: Label
- `('regca:HashRateContributedToNetwork', 'Documentation', 'en')`: Label
- `('regca:TotalNetworkHashRate', 'Documentation', 'en')`: Label
- `('regca:BlockchainNetworkParticipationExpenses', 'Documentation', 'en')`: Label
- `('regca:AffiliateEngagedInBlockchainNetworkParticipationIndicator', 'Documentation', 'en')`: Label
- `('regca:AffiliateControlDirection', 'Documentation', 'en')`: Label
- `('regca:AffiliateControlBasis', 'Documentation', 'en')`: Label
- `('regca:NumberOfBlockchainNetworksOnWhichAffiliateParticipates', 'Documentation', 'en')`: Label
- `('regca:AffiliateTotalBlockchainNetworkParticipationExpenses', 'Documentation', 'en')`: Label
- `('regca:AffiliateParticipatesOnNetworkIndicator', 'Documentation', 'en')`: Label
- `('regca:AffiliateEffectiveStakeControlledOnNetwork', 'Documentation', 'en')`: Label
- `('regca:AffiliateHashRateContributedToNetwork', 'Documentation', 'en')`: Label
- `('regca:AffiliateNumberOfValidatorSlotsControlled', 'Documentation', 'en')`: Label
- `('regca:AffiliateBlockchainNetworkParticipationExpenses', 'Documentation', 'en')`: Label
- `('regca:TotalAffiliateBlockchainNetworkParticipationExpenses', 'Documentation', 'en')`: Label
- `('regca:NumberOfAffiliatesEngagedInBlockchainNetworkParticipation', 'Documentation', 'en')`: Label
- `('regca:AffiliatePerimeterCompletenessAttestationIndicator', 'Documentation', 'en')`: Label
- `('regca:AffiliatePerimeterAttestingOfficerName', 'Documentation', 'en')`: Label
- `('regca:AffiliatePerimeterAttestingOfficerTitle', 'Documentation', 'en')`: Label
- `('regca:AffiliatePerimeterAttestingOfficerRole', 'Documentation', 'en')`: Label
- `('regca:AffiliatePerimeterAttestingOfficerIdentifier', 'Documentation', 'en')`: Label
- `('regca:AffiliatePerimeterAttestationDate', 'Documentation', 'en')`: Label
- `('regca:CombinedStakeSharePercentageOnNetwork', 'Documentation', 'en')`: Label
- `('regca:CombinedHashPowerSharePercentageOnNetwork', 'Documentation', 'en')`: Label
- `('regca:CombinedValidatorSlotsControlledOnNetwork', 'Documentation', 'en')`: Label
- `('regca:IssuerCouldFulfillObligationsIfNetworkDisruptedIndicator', 'Documentation', 'en')`: Label
- `('regca:NetworkCongestionAffectsBothOperationsIndicator', 'Documentation', 'en')`: Label

## Rules-Nonstandard: records whose content differs

- `REGCA_REQ_1CRYPTO_ResponsibleSignatureDate`: Commentary, Rule
- `REGCA_COVER_01`: Commentary, Rule
- `REGCA_REQ_1CRYPTO_PreviousFilingMerkleRoot`: Commentary, Rule
- `REGCA_REQ_1CRYPTO_PreviousFilingDate`: Commentary, Rule
