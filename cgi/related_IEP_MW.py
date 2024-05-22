import sys
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import re

# check if command line arguments are provided
if len(sys.argv) < 2:
    print("USAGE: python3 related_IEP_MW.py <IEP lower limit (pH)> <IEP upper limit (pH)> <MW lower limit (Da)> <MW upper limit (Da)>")
    sys.exit(1)
else:
    # store command line arguments
    IEP_lower, IEP_upper = float(sys.argv[1]), float(sys.argv[2])
    MW_lower, MW_upper = float(sys.argv[3]), float(sys.argv[4])

# regerx to catch ambiguous protein sequences
pattern = re.compile(r"'[XBZJ]' is not a valid unambiguous letter for protein")

# parse protein sequences in FASTA file
for seq_record in SeqIO.parse("./data/uniprot-all.fasta", "fasta"):
    descr = seq_record.description
    try:
        # isoelectric point & calculate molecular weight
        protAnalysis = ProteinAnalysis(str(seq_record.seq))
        isoPoint = protAnalysis.isoelectric_point()
        molWeight = protAnalysis.molecular_weight()

    except ValueError as error:
        # skip unambiguous protein sequences
        if pattern.match(str(error)):
            continue
        else:
            raise
    
    # filter and return results
    if (MW_lower <= molWeight <= MW_upper) and (IEP_lower <= isoPoint <= IEP_upper):
        print(
            "Protein: {}\nIsoelectric Point: {}\tMolecular Weight: {}\n".format(
                descr, round(molWeight, 3), round(isoPoint, 3)))