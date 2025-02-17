from models.file_manager import * 
from models.utils import *
from tqdm import tqdm
from multiprocessing import Pool
from models.database import *

class CanImmune:
    def __init__(self) -> None:
        self.file_manager = logs()._init_logsFile()
        self.mutation_counter = MutationCounter()
        self.mutationFinder = MutationFinder()
        self.mutation_type = None
        # Define the process function here
    def process(self,idx,line):
        # implementation here
        fields = line.split('\t')
        # print(self._fields_len(fields))
        if self._fields_len(fields):
            self.mutation_type = "substitution"
            if self.mutation_type == "substitution":
                if self.mutationFinder._regexAA_Substitution(fields[10]):
                    self.mutation_counter.update("SUBSTITUTION_FOUND_counter", 1)
                    mutation_from, mutation_pos, mutation_to = self.mutationFinder._get_Substitution()

                
            # print(mutationFinder.Mutation_AA)
        # print(fields[0])
        self.mutation_counter.update("MAIN_count", idx)
        if idx % 50000 == 0:
            logs()._add_info(f"Processing line {idx}")
            # print(f"Processing line {idx}")
            # print(self.mutation_counter.counters)
            # print(f"Processing line {idx}")

    @staticmethod
    def processChunk(params):
        filename, chunk_number, number_of_chunks = params
        with open(filename, 'r') as fp:
            for idx, line in enumerate(tqdm(Files_Manager.file_block(fp, number_of_chunks, chunk_number), desc=f"Processing chunk {chunk_number}",unit=' mutations')):
                CanImmune().process(idx, line)

    def _fields_len(self,fields):
        if len(fields) == 26:
            return True
        else:
            return False
    
    
if __name__ == '__main__':
    fetch_refDBapi("grch37")
    filename = "/canelib/raw_data/COSMIC/CL/data/CellLinesProject_GenomeScreensMutant_v99_GRCh38.tsv"  # replace with your filename
    number_of_chunks = 4  # replace with the number of chunks you want

    li = [(filename, i, number_of_chunks) for i in range(number_of_chunks)]

    p = Pool()
    p.map(CanImmune.processChunk, li)


# #Multiple processes are created to process the file in parallel.
# CanImmune.processChunk(filename, 0, 4)

# Progress Output:
# Processing chunk 1: 1512610 mutations [00:36, 41521.13 mutations/s]
# Processing chunk 0: 1512489 mutations [00:36, 41177.01 mutations/s]
# Processing chunk 2: 1512994 mutations [00:36, 40974.24 mutations/s]
# Processing chunk 3: 1512896 mutations [00:37, 40790.19 mutations/s]


    