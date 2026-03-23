## CAN-IMMUNE — Data Analysis Branch

This branch contains the data analysis scripts and notebooks used in the CAN-IMMUNE manuscript for neoantigen identification in TNBC and melanoma immunopeptidomic datasets.

### Data

- **Immunopeptidomic raw data**: TNBC (MDA-MB-231) from PRIDE PXD023044; melanoma (LM-MEL-44, LM-MEL-53) from PRIDE PXD014397.
- **RNA-seq data**: MDA-MB-231 from NCBI GEO GSE163067.
- **Mutation sources**: COSMIC v100, CCLE 24Q2, published literature.
- **Mutant peptide libraries**: Generated using CAN-IMMUNE for cell line-specific, cancer type-specific, and tissue-level searches (see Supplementary Table S1).

### Pipeline

1. **Mutant peptide library search** -- LC-MS/MS raw data searched against CAN-IMMUNE libraries + UniProt reference proteome using FragPipe (MSFragger v4.2). Nonspecific digest, 20 ppm precursor tolerance, peptide length 7-25 aa, variable mods: oxidation (M), deamidation (NQ), N-term acetylation.
2. **Peptide rescoring** -- MSBooster + Percolator for FDR control at 1%. PeptideProphet probability > 0.9 filter applied.
3. **HLA binding prediction** -- NetMHCpan 4.1 against sample-specific HLA allotypes. Strong binder: %Rank_EL <= 0.5; weak binder: 0.5 < %Rank_EL < 2.
4. **Structural modelling** -- PANDORA for peptide-HLA complex prediction; AlphaFold2 for TCR:pHLA interaction modelling using CD8+ TIL-derived TCR sequences from Ham et al.
5. **Peptide ranking** -- Candidates ranked by binding affinity, spectral confidence, and structural features for prioritisation.

### Contents

- `analysis/dataprocessing.ipynb` -- Data processing for PEAKS Studio xPro output files at 1% and 100% FDR, rescoring, and comparison with MSFragger results.
- `can_immune_tools.ipynb` -- Utility notebook for working with CAN-IMMUNE libraries (mutation parsing, database lookups, peptide extraction).
- `src/` -- MutPep source code for mutant peptide library generation from MAF/VCF/COSMIC inputs.

### RNA-seq variant calling

BWA (v0.7.17) alignment to GRCh38 -> Samtools (v1.9) BAM conversion -> GATK (v4.1.4) duplicate marking and BQSR -> BCFtools (v1.20) variant calling (QUAL > 20) -> ANNOVAR annotation (refGene, ExAC, dbSNP, dbNSFP) -> non-synonymous SNV extraction and gene filtering against MDA-MB-231 expression data.

### Supplementary data files

- `Melanoma_all_predictions_20032025.csv` -- Melanoma mutant peptides identified across libraries.
- `TNBC_all_predictions_10062025.csv` -- TNBC mutant peptides identified across libraries.
- `TNBC_all_predictions_20032025_with_model_results.csv` -- MDA-MB-231 mutant peptides with pHLA and TCR model scores.
- `final_ranked_peptides_list.csv` -- Peptides ranked by binding, confidence, and structural features.

### Links

- CAN-IMMUNE platform: https://canelib.erc.monash.edu
- Main repository: https://github.com/sanjaysgk/CanImmune
- MutPep: https://github.com/sanjaysgk/Mutpep