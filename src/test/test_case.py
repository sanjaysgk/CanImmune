

# print(le)
import sys
sys.path.append('/canelib/CanImmuneTool/CanImmune/src')

from CanImmune import read_fasta, processChunk

ref_db_path = "test/data/SeqDB"
mut_file = "test/data/aliquot_ensemble_masked.maf"

# index the reference database
index_dict = read_fasta(ref_db_path)

# process the mutations
processChunk(mut_file, index_dict, 8, 4)


# # process the mutation files

# # default missense mutation
# # processChunk(mut_file, index_dict, 8, 4)

# # print(index_dict)

# processChunk(mut_file, index_dict, 8, 4,mutation_type='missense')

# processChunk(mut_file, index_dict, 8, 4,mutation_type='missense',regex='^p\.[A-Z][0-9]+[A-Z]$')
