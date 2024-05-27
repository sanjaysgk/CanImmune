from models.file_manager import * 
from tqdm import tqdm
from multiprocessing import Pool

class CanImmune:
    def __init__(self) -> None:
        self.file_manager = logs()._init_logsFile()
        # Define the process function here
    def process(self,idx,line):
        # implementation here
        if idx % 1000 == 0:
            logs()._add_info(f"Processing line {idx}")
            # print(f"Processing line {idx}")

    @staticmethod
    def processChunk(params):
        filename, chunk_number, number_of_chunks = params
        with open(filename, 'r') as fp:
            for idx, line in enumerate(tqdm(Files_Manager.file_block(fp, number_of_chunks, chunk_number), desc=f"Processing chunk {chunk_number}",unit=' mutations')):
                CanImmune().process(idx, line)

if __name__ == '__main__':
    filename = "/canelib/raw_data/COSMIC/CL/data/CellLinesProject_GenomeScreensMutant_v99_GRCh38.tsv"  # replace with your filename
    number_of_chunks = 10  # replace with the number of chunks you want

    li = [(filename, i, number_of_chunks) for i in range(number_of_chunks)]

    p = Pool()
    p.map(CanImmune.processChunk, li)