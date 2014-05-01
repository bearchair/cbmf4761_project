#! /usr/bin/python
import sys
import csv
from collections import defaultdict

dbsnp_dict = defaultdict()

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 29, 2014"

def usage():
    print """
        python query_dbsnp.py [init_vcf.txt] [pruned_dbsnp.txt]
        """

def load_dbsnp(dbsnp):
    l = dbsnp.readline()
    while l:
        parts = l.split('\t')
        key = (parts[0], parts[1], parts[3], parts[4])
        dbsnp_dict[key] = parts[2]
        l = dbsnp.readline()

def query(vcf):
    f = open("nondbsnp_vcf.txt", "w")
    e = open("test_further_vcf.txt", "w")
    l = vcf.readline()
    while l:
        g.write(l)
        parts = l.split('\t')
        if parts[2] != '.':
            e.write(l)
        else:
            check = (parts[0], parts[1], parts[3], parts[4])
            if check in dbsnp_dict:
                e.write(l)
            else:
                f.write(l)
        l = vcf.readline()
    f.close()
    e.close()

if len(sys.argv)!= 3:
    usage()
    sys.exit(2)

try:
    vcf = file(sys.argv[1],"r")
    dbsnp = file(sys.argv[2],"r")
    load_dbsnp(dbsnp)
    query(vcf)

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)