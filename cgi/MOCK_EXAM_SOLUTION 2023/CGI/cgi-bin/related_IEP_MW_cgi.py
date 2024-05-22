#!/usr/bin/env python3
import cgi, cgitb

from Bio import SeqIO
from Bio.SeqUtils import ProtParam
import sys
import re

multi_fasta_file = 'uniprot-all.fasta'

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
    print("<table border=1>")
    print("<tr><td>Protein ID</td><td>IEP (pH)</td><td>MW (Da)</td></tr>")
    for result in id_IEP_MW_table:
        if iep_lower_limit <= result[1] <= iep_upper_limit:
            if mw_lower_limit  <= result[2] <= mw_upper_limit:
                print("<tr><td>%s</td><td>%.2f</td><td>%.1F</td></tr>" % (result[0], result[1], result[2]))
    print("</table></body>\n")

# construct results table
id_IEP_MW_table = []
id_IEP_MW_table = prot_fasta_IEP_MW(multi_fasta_file, ambiguous_AA_regexp, verbous=0)

# generate results page
cgitb.enable()
print('Content-Type: text/html\n')
form = cgi.FieldStorage()
iep_lower_limit = float(form.getvalue('iepLower'))
iep_upper_limit = float(form.getvalue('iepUpper'))
mw_lower_limit = float(form.getvalue('mwLower'))
mw_upper_limit = float(form.getvalue('mwUpper'))

print('<html><body>Matching Proteins:<br/>')
retrieve_matching_proteins(id_IEP_MW_table, iep_lower_limit, iep_upper_limit, mw_lower_limit, mw_upper_limit)
print('</body></html>')

