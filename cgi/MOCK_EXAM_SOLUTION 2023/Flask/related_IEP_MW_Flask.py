from flask import Flask, render_template, request
import related_IEP_MW as PP
import re

multi_fasta_file = 'uniprot-all.fasta'

ambiguous_AA_regexp = re.compile(r'[XBZJ]')  # to identify sequences with ambiguous AA symbols (X:any,B:DN,Z:EQ,J:IL)

app = Flask(__name__)

@app.route("/")
def render_form():
    """Renders the form HTML"""
    return render_template("related_IEP_MW.html")


@app.route("/", methods=["POST"])
def results():
    """Returns the results with function(s) from related_IEP_MW.py script"""

    iep_lower_limit = float(request.form["iepLower"])
    iep_upper_limit = float(request.form["iepUpper"])
    mw_lower_limit = float(request.form["mwLower"])
    mw_upper_limit = float(request.form["mwUpper"])

    # construct results table
    id_IEP_MW_table = []
    id_IEP_MW_table = PP.prot_fasta_IEP_MW(multi_fasta_file, ambiguous_AA_regexp, verbous=0)

    out_str = "<table border=1>" + "<tr><td>Protein ID</td><td>IEP (pH)</td><td>MW (Da)</td></tr>"
    for result in id_IEP_MW_table:
        if iep_lower_limit <= result[1] <= iep_upper_limit:
            if mw_lower_limit  <= result[2] <= mw_upper_limit:
                out_str += ("<tr><td>%s</td><td>%.2f</td><td>%.1F</td></tr>" % (result[0], result[1], result[2]))
    out_str += "</table></body>"

    return out_str

if __name__ == '__main__':
    app.run(debug=True)
