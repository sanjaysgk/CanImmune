# Supplementary data

## Current — use this one

**`supplementary_data_V2_20260917.zip`** (8.5 MB)

Regenerated 2026-09-03 from CAN-IMMUNE v0.3 (COSMIC v104, DepMap 26Q1). This matches the
revised manuscript. Contains the five mutant peptide libraries searched in the case study
(Table S9) and the five prediction and ranking tables (Table S12), with `SHA256SUMS.txt`
and a README describing each file.

```bash
unzip supplementary_data_V2_20260917.zip
cd supplementary_data && shasum -a 256 -c SHA256SUMS.txt
```

## Superseded — do not use for the current manuscript

**`supplymentry_data-20260323T025830Z-3-001.zip`** (14.7 MB)

The v1 data, built on COSMIC v99 and CCLE 24Q2. Kept for provenance only. Its numbers
contradict the revised manuscript: it reports 822, 440 and 358 peptides where v2 reports
92, 156 and 80, and it predates the variant recurrence filter. It also uses the old
supplementary numbering, Table S1 and Table S4, for what are now Table S9 and Table S12.

## Elsewhere

| | |
|---|---|
| Full deposit, including search output | doi:10.5281/zenodo.22803271 |
| Raw mass spectrometry data | PRIDE PXD023044, PXD014397 |
| Library generator | https://github.com/sanjaysgk/MutPep |
| Platform | https://canelib.erc.monash.edu |
