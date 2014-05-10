#! /usr/bin/python
import sys
import csv
from collections import defaultdict

cosmic_dict = defaultdict(list)

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 25, 2014"

def usage():
    print """
        python query_cosmic.py [to_cosmic_vcf_names.txt] [Cosmic_database.txt]
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
    print 'COSMIC Database loaded into memory'

def query_cosmic(name, name_file):
    
    #this is the file which has data to extract
    root = './tocosmic_vcfs/'
    path = '%s%s' % (root, name)
    vcf_file = file(path, "r")

    #this is the file that will be written to
    name_parts = name.split('_')
    tumor_name = '%s_%s' % (name_parts[0], name_parts[1])
    write_file_name = './cosmic_queries/%s_cosmic_query.vcf' % tumor_name
    write_file = open(write_file_name, "w")

    name_file.write('%s_cosmic_query.vcf\n' % tumor_name)

    l = vcf_file.readline()
    while l:
        #include the headers regardless
        if l[0] == '#':
            write_file.write(l)
        #begin cosmic filtering
        else:
            parts = l.split('\t')
            gene_pos = '%s:%s' % (parts[0][3:], parts[1])
            if gene_pos in cosmic_dict:
                write_file.write('%s' % l)
        l = vcf_file.readline()
    write_file.close()
    print '%s checked against COSMIC db' % name

if len(sys.argv)!= 3:
    usage()
    sys.exit(2)

try:
    vcf_files = file(sys.argv[1],"r")
    cosmic_db = file(sys.argv[2],"r")
    name_file = open("./cosmic_queries/cosmic_query_names.txt", "w")
    load_cosmic(cosmic_db)
    for name in vcf_files:
        #remove newline character at the end of each line
        query_cosmic(name[:-1], name_file)
    name_file.close()
    print 'COSMIC filtration done'

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)