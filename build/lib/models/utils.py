import datetime
import re
import requests
import shutil
from tqdm import tqdm



class MutationCounter:
    def __init__(self):
        self.counters = {
            "MAIN_count": 0,
            "FILE_ERROR_counter": 0,
            "FILE_SUCCESS_counter": 0,
            "TRANSCRIPT_FOUND_counter": 0,
            "TRANSCRIPT_NOT_FOUND_counter": 0,
            "SUBSTITUTION_FOUND_counter": 0,
            "SUBSTITUTION_NOT_FOUND_counter": 0,
            "SUBSTITUTION_SUCCESS_counter": 0,
            "SUBSTITUTION_ERROR_counter": 0,
            "POSITION_FOUND_counter": 0,
            "POSITION_2ND_ATTEMPT_FOUND_counter": 0,
            "POSITION_3RD_ATTEMPT_FOUND_counter": 0,
            "POSITION_NOT_FOUND_counter": 0,
            "UNIPROTtoGRch38_NOT_FOUND_counter": 0,
            "MULTI_SEQ_FOUND_counter": 0,
            "MULTI_SEQ_POSITION_FOUND_counter": 0,
            "SUBSTITUTION_FOUND_2ND_ATTEMPT_counter": 0,
            "SUBSTITUTION_FOUND_3RD_ATTEMPT_counter": 0
        }

    def update(self, counter_name, value):
        if not isinstance(value, int):
            raise ValueError(f"Value must be an integer not {value}")
        if counter_name in self.counters:
            self.counters[counter_name] += value
        else:
            raise ValueError(f"Counter {counter_name} does not exist")

    def delete(self, counter_name):
        if counter_name in self.counters:
            del self.counters[counter_name]
        else:
            raise ValueError(f"Counter {counter_name} does not exist")

    def set_default(self, counter_name, value=0):
        self.counters[counter_name] = value
        

class MutationFinder:
    def __init__(self):
        self.Mutation_AA = None
        self.Mutation_CDS = None
        self.Mutation_from = None
        self.Mutation_to = None
        self.Mutation_pos = None
        
    def _regexAA_Substitution(self, Mutation_AA):
        assert isinstance(Mutation_AA, str), "Expected string for Mutation_AA"
        if re.match(r'^p\.[A-Z][0-9]+[A-Z]$',Mutation_AA):
            self.Mutation_AA = Mutation_AA
            return True
        else:
            return False
        
    def _get_Substitution(self):
        assert self.Mutation_AA is not None, "Mutation_AA is not set"
        assert re.fullmatch(r'^p\.[A-Z][0-9]+[A-Z]$', self.Mutation_AA) is not None, f"Mutation_AA Substitution is not valid format expected p.[A-Z][0-9]+[A-Z] got {self.Mutation_AA}"
        mutation_rex = re.search(r'p\.([A-Z])([0-9]+)([A-Z])', self.Mutation_AA)
        mutation_from = mutation_rex.group(1)
        mutation_pos = int(mutation_rex.group(2))
        mutation_to = mutation_rex.group(3)
        del self.Mutation_AA
        return mutation_from, mutation_pos, mutation_to
    
    def _get_peptide(self,mutation_seq, mutation_pos):
        # print(len(mutation_seq))
        mutation_pos = mutation_pos-1
        
        if len(mutation_seq) > 0:
            if mutation_pos <= 12:
                peptide = mutation_seq[0:mutation_pos] + mutation_seq[mutation_pos:mutation_pos+13]
            
            elif mutation_pos >= len(mutation_seq) - 12:
                peptide = mutation_seq[mutation_pos-12:mutation_pos-1] + mutation_seq[mutation_pos-1:len(mutation_seq)]
        
            # elif mutation_pos >= 12 and len(mutation_seq) <= 25:
            #     peptide = mutation_seq[mutation_pos-3:mutation_pos-1] + mutation_seq[mutation_pos-1:mutation_pos+13]
                
            else:
                peptide = mutation_seq[mutation_pos-12:mutation_pos-1] + mutation_seq[mutation_pos-1:mutation_pos+13]
            
            # # print(peptide)
            # if len(peptide) >16:
            # print(peptide)
            return peptide

    
class MutationValidator:
    def __init__(self, data: dict):
        assert isinstance(data["TRANSCRIPT_ACCESSION"], str), "Expected string for TRANSCRIPT_ACCESSION"
        assert isinstance(data["GENE_SYMBOL"], str), "Expected string for GENE_SYMBOL"
        assert isinstance(data["COSMIC_GENE_ID"], str), "Expected string for COSMIC_GENE_ID"
        assert isinstance(data["COSMIC_SAMPLE_ID"], str), "Expected string for COSMIC_SAMPLE_ID"
        assert isinstance(data["SAMPLE_NAME"], str), "Expected string for SAMPLE_NAME"
        assert isinstance(data["COSMIC_PHENOTYPE_ID"], str), "Expected string for COSMIC_PHENOTYPE_ID"
        assert isinstance(data["GENOMIC_MUTATION_ID"], str), "Expected string for GENOMIC_MUTATION_ID"
        assert isinstance(data["LEGACY_MUTATION_ID"], str), "Expected string for LEGACY_MUTATION_ID"
        assert isinstance(data["MUTATION_ID"], str), "Expected string for MUTATION_ID"
        assert isinstance(data["MUTATION_CDS"], str), "Expected string for MUTATION_CDS"
        assert isinstance(data["MUTATION_AA"], str), "Expected string for MUTATION_AA"
        assert isinstance(data["MUTATION_DESCRIPTION"], str), "Expected string for MUTATION_DESCRIPTION"
        assert isinstance(data["MUATION_TYPE"], str), "Expected string for MUATION_TYPE"
        assert isinstance(data["MUTATION_POS"], int), "Expected integer for MUTATION_POS"
        assert isinstance(data["MUTATION_FROM"], str), "Expected string for MUTATION_FROM"
        assert isinstance(data["MUTATION_TO"], str), "Expected string for MUTATION_TO"
        assert isinstance(data["RAW_SEQ"], str), "Expected string for RAW_SEQ"
        assert isinstance(data["MUTATION_FOUND"], bool), "Expected boolean for MUTATION_FOUND"
        assert isinstance(data["MUTATED_SEQ"], str), "Expected string for MUTATED_SEQ"
        assert isinstance(data["TRANSCRIPT_FOUND"], bool), "Expected boolean for TRANSCRIPT_FOUND"
        assert isinstance(data["MUTATION_RAWPOS"], int), "Expected integer for MUTATION_RAWPOS"
        assert isinstance(data["GENE_ACCESSION"], str), "Expected string for GENE_ACCESSION"
        assert isinstance(data["MULTI_SQ"], bool), "Expected boolean for MULTI_SQ"
        assert isinstance(data["PEPTIDE"], str), "Expected string for PEPTIDE"
        self.data = data



def dTime():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace("-", "").replace(" ", "").replace(":", ""))



def fetch_refDBapi(dbname):
    urls = {
        "grch37": "https://ftp.ensembl.org/pub/grch37/current/fasta/homo_sapiens/pep/Homo_sapiens.GRCh37.pep.all.fa.gz",
        "grch38": "https://ftp.ensembl.org/pub/release-112/fasta/homo_sapiens/pep/Homo_sapiens.GRCh38.pep.all.fa.gz"
    }
    DATABASE_DIR = "/canelib/CanImmuneTool/CanImmune/data"

    url = urls.get(dbname.lower())
    if url:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            filename = url.split('/')[-1]
            filepath = f"{DATABASE_DIR}/{filename}"
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(filepath, 'wb') as out_file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    out_file.write(data)
            progress_bar.close()
            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("ERROR, something went wrong")
            print(f"Downloaded {filename} to {DATABASE_DIR}")
        else:
            print(f"Failed to download {dbname}. HTTP Status Code: {response.status_code}")
    else:
        print(f"Database name {dbname} not recognized.")
# #call download refSeq database
# fetch_refDBapi("grch37")
# #download progress 
# 100%|██████████████| 12.8M/12.8M [00:51<00:00, 246kiB/s]



