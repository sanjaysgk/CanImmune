from models.file_manager import * 
from models.utils import *
from tqdm import tqdm
from multiprocessing import Pool

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
    filename = "/canelib/raw_data/COSMIC/CL/data/CellLinesProject_GenomeScreensMutant_v99_GRCh38.tsv"  # replace with your filename
    number_of_chunks = 4  # replace with the number of chunks you want

    li = [(filename, i, number_of_chunks) for i in range(number_of_chunks)]

    p = Pool()
    p.map(CanImmune.processChunk, li)