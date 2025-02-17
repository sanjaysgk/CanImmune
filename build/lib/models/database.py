from typing import List, Tuple, Dict, Set
from models.file_manager import *
from Bio import SeqIO
import concurrent.futures
import os
import re

class ProteinIDindex:
    def __init__(self):
        self.index = Dict[str, List[str]] = {}
        
    def add(self, protein_id: str, index: List[str]):
        self.index[protein_id] = index
        self.index[protein_id].sort()
        
    def remove(self, protein_id: str):
        del self.index[protein_id]
        
    def get(self, protein_id: str):
        return self.index[protein_id]
    
    def get_all(self):
        return self.index
    
    def get_all_keys(self):
        return self.index.keys()
    
def read_fasta(file_path):
    with open(file_path, 'r') as file:
        fasta_dict = {}
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                seq_id = line[1:]
                fasta_dict[seq_id] = ''
            else:
                fasta_dict[seq_id] += line
    return fasta_dict
import concurrent.futures


class RefseqDB:
    """A class for managing a reference sequence database."""

    def __init__(self):
        """Initialize an empty database."""
        self.db = {}

    @staticmethod
    def _process_chunk(chunk):
        """Process a chunk of lines from a file and return a dictionary mapping IDs to values."""
        db = {}
        for line in chunk:
            fields = line.split('\t')
            if len(fields) >= 2:
                db[fields[0]] = fields[1]
            else:
                logger.warning(f"Unexpected line format: {line}")
        return db
        
    def _read_data(self, file_path: str):
        """Read data from a file and store it in the database."""
        try:
            with open(file_path, 'r') as fp:
                lines = fp.readlines()
        except IOError:
            print(f"Error opening file: {file_path}")
            return

        chunks = [lines[i:i + 5000] for i in range(0, len(lines), 5000)]  # adjust chunk size as needed

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for chunk_db in executor.map(self._process_chunk, chunks):
                self.db.update(chunk_db)

    @staticmethod
    def read_fasta(file_path):
        """Read a FASTA file and return a dictionary mapping sequence IDs to sequences."""
        try:
            fasta_dict = {}
            for seq_record in SeqIO.parse(file_path, "fasta"):
                match = re.search(r'(ENST\d+(\.\d+)?)', seq_record.description)
                if match:
                    seq_record.id = match.group(1)
                    fasta_dict[str(seq_record.id).split('.')[0]] = str(seq_record.seq)
                else:
                    print("Not Matched")
                    del seq_records
                    # print(seq_rec)
            return fasta_dict
        except IOError:
                print(f"Error opening file: {file_path}")
                return {}

    def getRecord_ENST(self, record):
        """ Extract the ENST ID from a SeqRecord."""
        
        match = re.search(r'(ENST\d+(\.\d+)?)', record.description)
        if match is not None:
            try:
                assert "ENST" in str(match.group(1)), "ENST not found"
                # print("##"*10)
                del record
            except AssertionError:
                pass
            return str(match.group(1))
        else:
            return None

    def RefseqIndex(self, file_path):
        """Create an index of protein IDs from a FASTA file."""
        try:
            index_dict = SeqIO.to_dict(
                SeqIO.parse(file_path, "fasta"), key_function= self.getRecord_ENST
            )
            return index_dict
        except IOError:
            print(f"Error opening file: {file_path}")
            return {}

    def __str__(self):
        """Return a string representation of the database."""
        return str(self.db)


class SequenceDB:
    def __init__(self):
        self.db = Dict[str, str] = {}
    
    def _find_fileType(self):
        pass
   
   
   