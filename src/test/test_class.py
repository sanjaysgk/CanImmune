import unittest
from pathlib import Path
from models.database import RefseqDB
from models.inputfiles import maf_parser
from Bio.SeqRecord import SeqRecord
from models.utils import *
import re
import json
#export PYTHONPATH="${PYTHONPATH}:/canelib/CanImmuneTool/CanImmune/src"
class TestRefseqDB(unittest.TestCase):
    # def test_read_data(self):
    #     db = RefseqDB()
    #     db._read_data("/canelib/CanImmuneTool/CanImmune/data/SeqDB/Homo_sapiens.GRCh38.pep.all.fa")
    #     self.assertNotEqual(db.db, {})
 
        
    def test_read_fasta(self):
        # fasta_dict = RefseqDB.read_fasta("/canelib/CanImmuneTool/CanImmune/data/SeqDB/Homo_sapiens.GRCh38.pep.all.fa")
        # print(type(fasta_dict))
        # print(len(fasta_dict))


        # Path to the JSON file
        file_path_json = '/canelib/CanImmuneTool/CanImmune/data/index/enst_to_gene.json'

        # Reading the JSON file as a dictionary
        with open(file_path_json, 'r') as file:
            ENST_to_gene_data = json.load(file)
            
        
# Now, `data` is a dictionary containing the contents of enst_to_gene.json
        # for key, value in fasta_dict.items():
        #     print(value)
        refseq_db = RefseqDB()
        mut_finder = MutationFinder()
        # index_dict  = refseq_db.RefseqIndex("/canelib/CanImmuneTool/CanImmune/data/SeqDB/Homo_sapiens.GRCh38.pep.all.fa")
        index_dict = refseq_db.read_fasta("/canelib/CanImmuneTool/CanImmune/data/SeqDB/Homo_sapiens.GRCh38.pep.all.fa")
        # print(dict_file)
        filename = "/canelib/CanImmuneTool/CanImmune/data/test/wex_output/2da93a17-e1af-4cbb-b23f-25f7a701ca96/aliquot_ensemble_masked.maf"
        output_dir = "/canelib/CanImmuneTool/CanImmune/data/test/wex_output/2da93a17-e1af-4cbb-b23f-25f7a701ca96/"
        maf_parser_data =  maf_parser(filename,output_dir)
        # print(maf_parser_data.head())
        
        # HGVSp_Short , Transcript_ID
        # print(maf_parser_data[['HGVSp_Short','Transcript_ID']])
        source_id_file = {}
        with open("mutated_protein.fasta", "w") as fasta_file:
            for index, row in maf_parser_data.iterrows():
                # print(row)
                seq_ =''
                AA_mut = str(row['HGVSp_Short'])
                # match = re.search(r'p\.\w\d+\w', AA_mut)
                mut_id = mut_finder._regexAA_Substitution(AA_mut)
                ENST_ID = str(row['Transcript_ID'])
                gene_name = str(row['Hugo_Symbol'])
                # print(AA_mut,ENST_ID)
                if mut_id:
                    mutation_from, mutation_pos, mutation_to = mut_finder._get_Substitution()
                    if ENST_ID.split('.')[0] in index_dict:
                        seq_ = index_dict[ENST_ID.split('.')[0]]
                        fasta_header = f"<CANE-IMMUNE|ENST_ID_ENST_ID{ENST_ID}|Gene_name{gene_name}|Mutation_AA_{mut_id}|CANE-IMMUNE_{index}\n"
                        
    
                        # print(seq_)
                        # print(AA_mut)
                        # print(f"Mutation from {mutation_from} at position {mutation_pos} to {mutation_to}")
                        if seq_[mutation_pos+1] == mutation_from:
                            print(f"Mutation from {mutation_from} at position {mutation_pos} to {mutation_to}")
                            print(ENST_ID)
                            # Construct the mutated protein sequence
                            mut_protien = seq_[:mutation_pos] + mutation_to + seq_[mutation_pos+1:]
                            mutpep = mut_finder._get_peptide(mut_protien, mutation_pos)
                            print(mutpep)
                            fasta_file.write(fasta_header)
                            fasta_file.write(f"{mutpep}\n")
                            source_id_file[f'CANE_IMMUNE_{index}'] = ''.join(str(item) for item in row)
                            # row
                        elif seq_[mutation_pos+1] == mutation_from:
                            for enst_ids, gene_ids in ENST_to_gene_data.items():
                                if gene_name == gene_ids:
                                    # print(f"Gene name {gene_ids}")
                                    seq_ = index_dict[enst_ids]
                                    print("$$$$")
                                    if mutation_pos < len(seq_) and seq_[mutation_pos+1] == mutation_from:
                                        print("#########")
                                        source_id_file[f'CANE-IMMUNE_{index}'] = ''.join(row)
                                        fasta_file.write(f"{mut_protien}\n")
                            # print(gene_name)
        print(source_id_file)        
        # for key, value in index_dict.items():
        #     print(value)
        #     # match = re.search(r"Seq\(\'(.*)\'\)", value)
            # if match:
            #     print(match.group(1))
if __name__ == '__main__':
    unittest.main()
refseq_db = RefseqDB()



    
# def processChunk(params):
#     filename, chunk_number, number_of_chunks = params
#     with open(filename, 'r') as fp:
#         for idx, line in enumerate(tqdm(Files_Manager.file_block(fp, number_of_chunks, chunk_number), desc=f"Processing chunk {chunk_number}",unit=' mutations')):
#             CanImmune().process(idx, line)
    
# from CanImmune import read_fasta, processChunk
# #reference database path
# ref_db_path = "test/data/SeqDB"

# #path to the maf, vcf or tsv file
# mut_file = "test/data/aliquot_ensemble_masked.maf"

# #index the reference database
# index_dict = read_fasta(ref_db_path)

# #process the mutation files
# #default missense mutation
# processChunk(mut_file,index_dict, 8, 4)

# #missense mutation with specific mutation type
# processChunk(mut_file,index_dict, 8, 4, mutation_type="missense")

# #missense mutation with specific mutation type and specific regex
# processChunk(mut_file,index_dict, 8, 4, regex="^p\.[A-Z][0-9]+[A-Z]$")



