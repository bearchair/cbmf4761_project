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
    f = open("filtered_vcf.txt", "w")
    ref_len = 0
    reference = ''
    while l:
        if l[0] == '#':
            if l[1] != '#':
                reference = l.split('\t')
                reference[0] = reference[0][1:]
                reference[9] = reference[9][:-2]
                ref_len = len(reference)
                f.write('VCF')
                i = 0
                while i < 2:
                    f.write('\t')
                    i = i+1
                f.write('\n')
                i = 0
                while i < 2:
                    f.write('%s\t' % reference[i])
                    i = i+1
                f.write('\n')
        else:
            parts = l.split('\t')
            if parts[6] == 'PASS':
                chrom_pos = '%s\t%s\n' % (parts[0], parts[1])
                f.write(chrom_pos)
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

