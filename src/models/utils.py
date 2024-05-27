import datetime

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