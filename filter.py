#! /usr/bin/python
import sys
import vcf
from collections import defaultdict
import csv

#dictionaries
SeattleSeq_pos = defaultdict()
cosmic_pos = defaultdict()
Omim_pos = defaultdict()
vcf_info = []

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 4, 2014"

def usage():
    print """
        python filter.py [Mutation_Report.txt] [SeattleSeq_database.txt] [Cosmic_database.txt] [omim.txt]
        """

def load_SeattleSeq(SeattleSeq_database, SeattleSeq_pos):
    l = SeattleSeq_database.readline()
    reference = l.split('\t')
    ref_len = len(reference)
    reference[ref_len-1] = reference[ref_len-1][0:-2]
    l = SeattleSeq_database.readline()
    f = open("formatted_SS.txt", "w")
    #rudimentary version of loading the data file, the point is that it can be loaded in whichever way we need
    while l:
        parts = l.split('\t')
        i = 0
        if parts[0][0] != '#':
            while i < len(reference):
                f.write('%s : %s\n' % (reference[i], parts[i]))
                i = i + 1
            f.write('\n')
        l = SeattleSeq_database.readline()
    f.close()

def load_Cosmic(Cosmic_database, cosmic_pos):
    l = Cosmic_database.readline()
    reference = l.split('\t')
    ref_len = len(reference)
    reference[ref_len-1] = reference[ref_len-1][0:-2]
    l = Cosmic_database.readline()
    f = open("formatted_Cosmic.txt", "w")
    e = open("Cosmic_errors.txt", "w")
    #rudimentary version of loading the data file, the point is that it can be loaded in whichever way we need
    while l:
        parts = l.split('\t')
        check = len(parts)
        if ref_len != check:
            i = 0
            while i < len(parts):
                e.write('%s\n' % parts[i])
                i = i + 1
            e.write('\n')
        else:
            i = 0
            while i < len(reference):
                f.write('%s : %s\n' % (reference[i], parts[i]))
                i = i + 1
            f.write('\n')
        l = Cosmic_database.readline()
    f.close()

#def load_Omim(Omim_database, Omim_pos):



def load_vcf(vcf_file, vcf_info):
    l = vcf_file.readline()
    f = open("formatted_vcf.txt", "w")
    ref_len = 0
    reference = ''
    while l:
        if l[0] == '#':
            if l[1] != '#':
                reference = l.split('\t')
                reference[0] = reference[0][1:]
                reference[9] = reference[9][:-2]
                ref_len = len(reference)
                print reference
        else:
            parts = l.split('\t')
            i = 0
            while i < len(reference):
                f.write('%s : %s\n' % (reference[i], parts[i]))
                i = i + 1
            f.write('\n')
            print parts
        l = vcf_file.readline()
    f.close()


if len(sys.argv)!= 5:
    usage()
    sys.exit(2)

try:
    snp_list = file(sys.argv[1],"r")
    load_vcf(snp_list, vcf_info)
    SeattleSeq_database = file(sys.argv[2],"r")
    load_SeattleSeq(SeattleSeq_database, SeattleSeq_pos)
    Cosmic_database = file(sys.argv[3],"r")
    load_Cosmic(Cosmic_database, cosmic_pos)
    #Omim_database = file(sys.argv[4]. "r")
    #load_Omim(Omim_database, Omim_pos)

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)