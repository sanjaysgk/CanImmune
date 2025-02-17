import pandas as pd
import os
import openpyxl
import unittest
from pathlib import Path
from models.database import RefseqDB
from models.inputfiles import maf_parser
from Bio.SeqRecord import SeqRecord
from models.utils import *
import re
import json
import pandas as pd

def _data_extract(file, gene_mapped):
    refseq_db = RefseqDB()
    index_dict = refseq_db.read_fasta("/canelib/CanImmuneTool/CanImmune/data/refData/grch38/Homo_sapiens.GRCh38.pep.all.fa")

    data = pd.read_excel(file)
    mut_finder = MutationFinder()
    with open(gene_mapped, 'r') as f:
        gene_list = json.load(f)
    
    # Initialize an empty DataFrame with desired columns
    columns = list(data.columns) + ['Peptide']
    results_df = pd.DataFrame(columns=columns)
    new_rows = []
    
    for index, row in data.iterrows():
        if 'snv' in str(row['ExonicFunc.refGene']).lower():
            AA_mut = str(row['AAChange.refGene'])
            AA_mut_list = AA_mut.split(',')
            ENST_list = []
            for enst, gene in gene_list.items():
                if str(row['Gene.refGene']).lower() == str(gene).lower():
                    ENST_list.append(enst)
            p_aa = ''
            for protein_mut in AA_mut_list:
                if p_aa != protein_mut.split(':')[-1]:
                    p_aa = protein_mut.split(':')[-1]
                    mut_id = mut_finder._regexAA_Substitution(p_aa)
                    if mut_id:
                        mutation_from, mutation_pos, mutation_to = mut_finder._get_Substitution()
                        for ENST in ENST_list:
                            if str(ENST).split('.')[0] in index_dict:
                                seq_ = index_dict[ENST.split('.')[0]]
                                if len(seq_) > mutation_pos+1:
                                    if seq_[mutation_pos+1] == mutation_from:
                                        muste_seq = seq_[:mutation_pos+1] + mutation_to + seq_[mutation_pos+2:]
                                        peptide = mut_finder._get_peptide(muste_seq, mutation_pos)
                                        # Create a new row with the same data as the current row plus the peptide
                                        new_row = row.to_dict()
                                        new_row['Peptide'] = peptide
                                        new_rows.append(new_row)  # Append the new_row dictionary to the list
                                        
    final_df = pd.DataFrame(new_rows)
    print(len(final_df['Peptide'].unique()))
    # Now, write this DataFrame to a CSV file
    final_df.to_csv('/canelib/CanImmuneTool/CanImmune/data/test/wex_output/output_IBC_Mutpeptids.csv', index=False)
    
file = "/canelib/CanImmuneTool/CanImmune/data/test/wex_output/IBC_WES_mutation_info.xlsx"
gene_mapped = "/canelib/CanImmuneTool/CanImmune/data/index/enst_to_gene.json"

# _data_extract(file, gene_mapped)

df = pd.read_csv('/canelib/CanImmuneTool/CanImmune/data/test/wex_output/output_IBC_Mutpeptids.csv')

print(len(df['Peptide'].unique()))
print(len(df['Gene.refGene'].unique()))