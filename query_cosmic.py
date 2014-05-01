#! /usr/bin/python
import sys
import csv
from collections import defaultdict

cosmic_dict = defaultdict(list)

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 25, 2014"

def usage():
    print """
        python query_cosmic.py [filtered_vcf.txt] [Cosmic_database.txt]
        """

def load_cosmic(cosmic_db):
    l = cosmic_db.readline()
    l = cosmic_db.readline()
    while l:
        parts = l.split('\t')
        if len(parts) == 15:
            gene_pos = parts[13]
            pos_range = gene_pos.split('-')
            if len(pos_range) > 1:
                if pos_range[0].split(':')[1] == pos_range[1]:
                    pos_string = '%s' % pos_range[0]
                    cosmic_dict[pos_string] = parts[0]
        l = cosmic_db.readline()

def query_cosmic(vcf_file):
    f = open("cosmic_queries.txt", "w")
    l = vcf_file.readline()
    while l:
        parts = l.split('\t')
        gene_pos = '%s:%s' % (parts[0], parts[1])
        if gene_pos in cosmic_dict:
            f.write('%s' % l)
        l = vcf_file.readline()
    f.close()

if len(sys.argv)!= 3:
    usage()
    sys.exit(2)

try:
    vcf_file = file(sys.argv[1],"r")
    cosmic_db = file(sys.argv[2],"r")
    load_cosmic(cosmic_db)
    query_cosmic(vcf_file)

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)