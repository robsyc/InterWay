from Bio import SeqIO
from Bio.SeqUtils import ProtParam
import sys
import re

ambiguous_AA_regexp = re.compile(r'[XBZJ]')  # to identify sequences with ambiguous AA symbols (X:any,B:DN,Z:EQ,J:IL)


def prot_fasta_IEP_MW( multi_fasta_file, ambiguous_AA_regexp, verbous = 0 ):
    id_IEP_MW_table = []
    handle = open( multi_fasta_file )
    for record in SeqIO.parse(handle, "fasta"):
        seq = str(record.seq)
        if not ambiguous_AA_regexp.search(seq): # process only unambiguous protein sequences
            X = ProtParam.ProteinAnalysis(seq)

            IEP = X.isoelectric_point()
            MW = X.molecular_weight()

            if verbous:
                print("%s\t%.2f\t%.1f" % (record.description, IEP, MW))

            id_IEP_MW_table.append([record.description, IEP, MW])

    return( id_IEP_MW_table )


def retrieve_matching_proteins(id_IEP_MW_table, iep_lower_limit, iep_upper_limit, mw_lower_limit, mw_upper_limit):
    for result in id_IEP_MW_table:
        if iep_lower_limit <= result[1] <= iep_upper_limit:
            if mw_lower_limit  <= result[2] <= mw_upper_limit:
                print("%s\t%.2f\t%.1f" % (result[0], result[1], result[2]))


if __name__ == '__main__':

    if not len(sys.argv) == 5:
        sys.stderr.write("USAGE: python3 %s < IEP lower limit (pH) > < IEP upper limit (pH) > < MW lower limit (Da) > < MW upper limit (Da) >\n" % sys.argv[0])
        sys.exit(1)

    multi_fasta_file = 'uniprot-all.fasta'

    iep_lower_limit = float(sys.argv[1])
    iep_upper_limit = float(sys.argv[2])
    mw_lower_limit = float(sys.argv[3])
    mw_upper_limit = float(sys.argv[4])

    id_IEP_MW_table = []
    try:
        id_IEP_MW_table = prot_fasta_IEP_MW(multi_fasta_file, ambiguous_AA_regexp, verbous=0)
    except FileNotFoundError:
        print(multi_fasta_file, " not existing or not readable! Check please...")

    retrieve_matching_proteins(id_IEP_MW_table, iep_lower_limit, iep_upper_limit, mw_lower_limit, mw_upper_limit)

