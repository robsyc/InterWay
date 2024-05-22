#!/usr/bin/env python
# related_IEP_MW_CGI.py
import cgi, cgitb
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import re

# regerx to catch ambiguous protein sequences
pattern = re.compile(r"'[XBZJ]' is not a valid unambiguous letter for protein")

cgitb.enable()
print('Content-Type: text/html\n')
form = cgi.FieldStorage()

# get arguments from form
job = form.getvalue('job')
IEP_lower, IEP_upper = float(form.getvalue('IEP_lower')), float(form.getvalue('IEP_upper'))
MW_lower, MW_upper = float(form.getvalue('MW_lower')), float(form.getvalue('MW_upper'))

print(f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Protein Finder</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Bootstrap styling in css folder -->
        <!-- <link href="css/bootstrap.min.css" rel="stylesheet"> -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body style="background-color:#e5ffdb;">
        <div class="container">
            <h1>Protein Finder</h1>
            <p class="lead">Query the Human UniprotKB <abbr title="Isoelectric Point (pH)">IP</abbr> and <abbr title="Molecular Weight (Da)">MW</abbr> database.</p>
            <hr>
            <h4>Query Parameters:</h4>
            <div class="row">
                <p class="fw-bold col-sm-2">Job ID: </p>
                <p class="col-sm-10">{job}</p>
            </div>
            <div class="row">
                <p class="fw-bold col-sm-2">Isoelectric point (pH): </p>
                <p class="col-sm-10">{IEP_lower} - {IEP_upper}</p>
            </div>
            <div class="row">
                <p class="fw-bold col-sm-2">Molecular weight (Da): </p>
                <p class="col-sm-10">{MW_lower} - {MW_upper}</p>
            </div>
            <hr>
            <h4>Matching Proteins:</h4>
""")

# parse protein sequences in FASTA file
i = 0
for seq_record in SeqIO.parse("./data/uniprot-all.fasta", "fasta"):
    id = seq_record.id
    descr = seq_record.description[len(id):]
    try:
        # calculate isoelectric point & molecular weight
        protAnalysis = ProteinAnalysis(str(seq_record.seq))
        isoPoint = protAnalysis.isoelectric_point()
        molWeight = protAnalysis.molecular_weight()

    except ValueError as error:
        # skip unambiguous protein sequences
        if pattern.match(str(error)):
            continue

    # filter and return results
    if (MW_lower <= molWeight <= MW_upper) and (IEP_lower <= isoPoint <= IEP_upper):
        i += 1
        print(f"""
            <div class="card">
                <div class="card-header">
                    <div class="row">
                        <div class="col-2 text-end">
                            Protein ID:
                        </div>
                        <div class="col-10">
                            {id}
                        </div>
                    </div>
                </div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">
                        <div class="row">
                            <div class="col-2 text-end">
                                Protein Description:
                            </div>
                            <div class="col-10">
                                {descr}
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item">
                        <div class="row">
                            <div class="col-2 text-end">
                                Isoelectric Point (pH):
                            </div>
                            <div class="col-10">
                                {round(isoPoint, 3)}
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item">
                        <div class="row">
                            <div class="col-2 text-end">
                                Molecular Weight (Da):
                            </div>
                            <div class="col-10">
                                {round(molWeight, 3)}
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
            <br>
        """)

print(f"""
            <hr>
            <br>
            <p>Number of matches: {i}</p>
            <br>
        </div>
    </body>
    <div class="container">
        <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
            <span class="text-muted">Programming for Bioinformatics - 2022</span>
            <span class="text-muted">Robbe Claeys</span>
            <a class="text-muted" href="https://github.com/robsyc"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg></a>
        </footer>
    </div>
</html>
""")