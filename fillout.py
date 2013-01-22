#!/usr/bin/python
#
# Fills FDF-able fields of PDFs with a JSON file, and provides
# orientation by displaying field names inline.
# (c) 2012-2013 Rudolf M. Schreier <rms@vis.ethz.ch>

from fdfgen import forge_fdf
import subprocess
import argparse
import json

description =\
"""Fills the fields of the provided PDF 'infile' with the values provided (as JSON)
in 'json_file', and renders the result into a PDF 'outfile'.
If 'json_file' is not provided, 'outfile' will print the field names of all available
fields in their respective spot in the PDF.
"""

search_token = "FieldName:"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-f', metavar="json_file", help="JSON file containing value pairs "
                            "of 'field_name': 'field_value'")
    parser.add_argument('-i', required=True, metavar="infile", help="Input PDF file")
    parser.add_argument('-o', required=True, metavar="outfile", help="Output PDF file")
    args = parser.parse_args()

    if args.f:
        print "Filling fields..."
        with open(args.f, 'r') as json_file:
            parsed_json = json.loads(json_file.read())
            fields = [(k,v,) for k,v in parsed_json.iteritems()]

    else:
        print "Dumping field names as PDF..."
        raw_lines = subprocess.check_output(["pdftk", args.i, "dump_data_fields"]).splitlines()
        fields = []
        for raw_line in raw_lines:
            if search_token in raw_line:
                token = raw_line[len(search_token)+1:]
                fields.append((token, token,))

    fdf = forge_fdf("", fields, [], [], [])
    p = subprocess.Popen(["pdftk", args.i, "fill_form", "-",
                       "output", args.o, "flatten"], stdin=subprocess.PIPE)
    p.communicate(fdf)
