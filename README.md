## CAN-IMMUNE

A computational platform for cancer-specific immunopeptidomics-based neoantigen identification and evaluation.

CAN-IMMUNE allows users to browse, search, and generate bespoke mutant peptide libraries for LC-MS/MS database searching across 33 cancer types.

### Data

- **Mutation sources**: COSMIC (v100), CCLE (24Q2), and published literature.
- **Scale**: 6,721,816 cancer-specific missense substitutions from 1,460 cell lines, 43 tissue sites, and 19,768 genes.
- **Output**: 1,194,608 unique mutant peptides (25 amino acids each, 12 flanking residues on each side of the mutation).
- Mutations are cross-referenced against RefSeq (GRCh38) and UniProt for validation.

### Pipeline

1. **Mutation data collection** -- Missense substitutions extracted from COSMIC, CCLE, and literature; cross-referenced with RefSeq and UniProt.
2. **Mutant peptide generation** -- For each validated mutation, a 25-aa peptide is extracted (12 residues upstream and downstream of the mutated position).
3. **MutPep** -- Standalone Python tool for generating custom mutant peptide libraries from user-provided data (MAF, VCF, COSMIC, or custom mutation lists). Uses multiprocessing for large datasets.
4. **LC-MS/MS search** -- Generated libraries are used with search engines (FragPipe/MSFragger, PEAKS, DIA-NN) against immunopeptidomic raw data.
5. **Peptide rescoring** -- Percolator and MSBooster for FDR control; PeptideProphet probability > 0.9 filter.
6. **HLA binding prediction** -- NetMHCpan 4.1 predicts peptide-HLA binding affinity (%Rank_EL <= 0.5 = strong binder).
7. **Structural analysis and ranking** -- PANDORA for peptide-HLA complex modelling; AlphaFold2 for TCR:pHLA interaction prediction. Peptides ranked by binding affinity, spectral confidence, and structural features.

### RNA-seq workflow (optional)

For sample-specific mutation calling: BWA alignment -> Samtools/GATK processing -> BCFtools variant calling -> ANNOVAR annotation -> custom mutant database generation. See supplementary materials for details.

### Installation

```bash
pip install -r requirements.txt
```

### Links

- Platform: https://canelib.erc.monash.edu
- MutPep: https://github.com/sanjaysgk/Mutpep
- Data analysis scripts: https://github.com/sanjaysgk/CanImmune/tree/data-analysis