#! /usr/bin/python
import sys
import csv

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 29, 2014"

def usage():
    print """
        python filter_vcf.py [dbsnp_132_b37.leftAligned.txt]
        """

def filter(vcf_file):
    l = vcf_file.readline()
    f = open("pruned_dbsnp.txt", "w")
    ref_len = 0
    reference = ''
    while l:
        if l[0] != '#':
            parts = l.split('\t')
            i = 0
            while i < 6:
                f.write('%s\t' % parts[i])
                i = i+1
            f.write('\n')
        l = vcf_file.readline()
    f.close()

if len(sys.argv)!= 2:
    usage()
    sys.exit(2)

try:
    dbsnp_file = file(sys.argv[1],"r")
    filter(dbsnp_file)

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)

