#! /usr/bin/python
import sys
import csv
from collections import defaultdict

dbsnp_dict = defaultdict()

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 29, 2014"

def usage():
    print """
        python query_dbsnp.py [passed_vcf_names.txt] [pruned_dbsnp.txt]
        """

def load_dbsnp(dbsnp):
    l = dbsnp.readline()
    while l:
        parts = l.split('\t')
        #chromosome, position number, reference allele, and allele mutation
        key = (parts[0], parts[1], parts[3], parts[4])
        #dbsnp id
        dbsnp_dict[key] = parts[2]
        l = dbsnp.readline()

def query(name, name_file_one, name_file_two):

    #this is the file which has data to extract
    root = './passed_vcfs/'
    path = '%s%s' % (root, name)
    vcf_file = file(path, "r")
    
    #these are the files that will be written to
    name_parts = name.split('_')
    tumor_name = '%s_%s' % (name_parts[0], name_parts[1])
    write_file_name_one = './nondbsnp_vcfs/%s_nondbsnp.vcf' % tumor_name
    write_file_name_two = './tocosmic_vcfs/%s_tocosmic.vcf' % tumor_name
    nondbsnp_file = open(write_file_name_one, "w")
    tocosmic_file = open(write_file_name_two, "w")
    
    #these are the files that will serve as indices for future python calls in map_mutations.sh
    name_file_one.write('%s_nondbsnp.vcf\n' % tumor_name)
    name_file_two.write('%s_tocosmic.vcf\n' % tumor_name)

    
    l = vcf_file.readline()
    while l:
        #include the headers regardless
        if l[0] == '#':
            nondbsnp_file.write(l)
            tocosmic_file.write(l)
        #begin dbsnp filtering
        else:
            parts = l.split('\t')
            #if a dbsnp id is already included in the vcf entry, there's no need to query the dictionary
            if parts[2] != '.':
                tocosmic_file.write(l)
            #otherwise, we need to query
            else:
                check = (parts[0][3:], parts[1], parts[3], parts[4])
                if check in dbsnp_dict:
                    tocosmic_file.write(l)
                else:
                    nondbsnp_file.write(l)
        l = vcf_file.readline()
    nondbsnp_file.close()
    tocosmic_file.close()

if len(sys.argv)!= 3:
    usage()
    sys.exit(2)

try:
    vcf_files = file(sys.argv[1],"r")
    dbsnp = file(sys.argv[2],"r")
    name_file_one = open("./nondbsnp_vcfs/nondbsnp_vcf_names.txt", "w")
    name_file_two = open("./tocosmic_vcfs/tocosmic_vcf_names.txt", "w")
    load_dbsnp(dbsnp)
    for name in vcf_files:
        #remove newline character at the end of each line
        query(name[:-1], name_file_one, name_file_two)
    name_file_one.close()
    name_file_two.close()

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)