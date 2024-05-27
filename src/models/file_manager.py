import logging
from utils import dTime
logger = logging.getLogger(__name__)
import os

class Files_Manager:
    def __init__(self):
        self.file = None
    def check_file(self):
        return self.file
    #https://stackoverflow.com/questions/40745686/python-process-file-using-multiple-cores
    @staticmethod
    def file_block(fp, number_of_blocks, block):
        '''
        A generator that splits a file into blocks and iterates
        over the lines of one of the blocks.

        '''

        assert 0 <= block and block < number_of_blocks
        assert 0 < number_of_blocks

        fp.seek(0,2)
        file_size = fp.tell()

        ini = file_size * block / number_of_blocks
        end = file_size * (1 + block) / number_of_blocks

        if ini <= 0:
            fp.seek(0)
        else:
            fp.seek(ini-1)
            fp.readline()

        while fp.tell() < end:
            yield fp.readline()
            
            
    def _find_fileType(self):
        if len(self.file.split('.')) > 1:
            return self.file.split('.')[-1]
        else:
            raise ValueError("File type not found")
    
    def check_permission(self):
        return self.file.mode
    
    def check_file_name(self):
        return self.file.name
    
    def check_file_encoding(self):
        return self.file.encoding
    
    def check_file_type(self):
        return self.file.mode
            
    def open_file(self, file_path):
        self.file = open(file_path, 'r')
        return self.file

    def read_file(self):
        return self.file.read()

    def close_file(self):
        self.file.close()
        self.file = None

class logs:
    def __init__(self):
        self.cwd = os.getcwd()
        self.logs = None
        self.dTime = dTime()
    def _init_logsFile(self):
        file_path = os.path.join(self.cwd, f'{self.dTime}_logs.txt')
        logging.basicConfig(filename=file_path, filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    def _add_info(self, info):
        logging.info(info)
    
    def _add_error(self, error):
        logging.error(error)
        
    def _add_warning(self, warning):
        logging.warning(warning)
        
    def _add_debug(self, debug):
        logging.debug(debug)
        

if __name__ == '__main__':
    manager = Files_Manager()
    manager.file = "enst_to_gene.json"
    manager._find_fileType()