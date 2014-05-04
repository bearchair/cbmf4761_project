#! /usr/bin/python
import sys
import csv

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 26, 2014"

def usage():
    print """
        python filter_vcf.py [2_Mutation_Report.txt]
        """

def filter(vcf_file):
    l = vcf_file.readline()
    f = open("init_vcf.txt", "w")
    while l:
        if l[0] != '#':
            parts = l.split('\t')
            if parts[6] == 'PASS':
                f.write(l)
        l = vcf_file.readline()
    f.close()

if len(sys.argv)!= 2:
    usage()
    sys.exit(2)

try:
    vcf_file = file(sys.argv[1],"r")
    filter(vcf_file)

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)