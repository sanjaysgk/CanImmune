
import os
# import maflib 
import sys
import pandas as pd
# sys.path.append('/canelib/CanImmuneTool/CanImmune/tools/maf-lib/')
# # import maflib 
# from maflib.reader import MafReader
# from Bio import AlignIO
# filename = "/canelib/CanImmuneTool/CanImmune/data/test/wex_output/2da93a17-e1af-4cbb-b23f-25f7a701ca96/aliquot_ensemble_masked.maf" 

# file = MafReader(filename)

# header = file.header()
# print(header)

def maf_parser(filename,output_dir):
    """
    This function is used to parse the MAF file, ensuring each line has the same number of fields as the header.
    Lines with a different number of fields are tagged as error lines and written to the output file.
    """
    
    # filename = "/canelib/CanImmuneTool/CanImmune/data/test/wex_output/2da93a17-e1af-4cbb-b23f-25f7a701ca96/aliquot_ensemble_masked.maf"
    # output_dir = "/canelib/CanImmuneTool/CanImmune/data/test/wex_output/2da93a17-e1af-4cbb-b23f-25f7a701ca96/"
    base_filename = os.path.basename(filename)
    output_filename = os.path.splitext(base_filename)[0] + "_parsed.tsv"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(filename, 'r') as raw_file, open(output_path, 'w') as output_file:
        header = next(raw_file).strip()  # Read the first line to get the header
        if header.startswith('#'):  # Skip initial comments to find the actual header
            for line in raw_file:
                if not line.startswith('#'):
                    header = line.strip()
                    break
        
        header_fields_count = len(header.split('\t'))
        # Write the header to the output file
        output_file.write(header + '\n')
        
        for line in raw_file:
            if not line.startswith('#'):  # Skip comment lines
                fields = line.strip().split('\t')
                if len(fields) == header_fields_count:
                    output_file.write('\t'.join(fields) + '\n')  # Write to output file
                else:
                    output_file.write(f"Error line: {line.strip()}\n")  # Tag as an error line and write to output file
    pandas_df = pd.read_csv(output_path, sep='\t')
    return pandas_df
# maf_parser()