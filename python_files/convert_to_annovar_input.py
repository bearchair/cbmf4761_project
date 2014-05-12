#! /usr/bin/python
import sys
import csv

# convert_to_annovar_input.py
#
# Due to difficulties getting the simulated non-cancerous exome sequencing
# to be properly processed during ANNOVAR gene annotation, this function was
# written to take the information found within the vcf file and convert it into
# another form which we can more easily assure will be read correctly. It is a
# simple tab-delimited file with five columns denoting chromosome, read start
# position, read end position, reference allele, and allele read.
#

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$May 10, 2014"

def usage():
    print """
        python convert_to_annovar_input.py [final_vcf.txt] [root]
        """

#this function handles the actual conversion process from a VCF file to a five column tab delimited file
def convert(name, name_file, root):
    path = '%s%s' % (root, name)
    read_file = file(path, "r")
    
    #the .human extension is a convention that seems to be used by ANNOVAR (referencing their example files found on the website)
    name_parts = name.split('.')
    write_name = '%s.human' % name_parts[0]
    write_path = './simulated_final_data/%s' % write_name
    write_file = open(write_path, "w")
    
    name_file.write('%s\n' % write_name)
    
    l = read_file.readline()
    while l:
        #we do not need headers in annovar 5-column input format
        if l[0] != '#':
            parts = l.split('\t')
            parts[0] = parts[0][3:]
            row = '%s\t%s\t%s\t%s\t%s\n' % (parts[0], parts[1], parts[1], parts[3], parts[4])
            write_file.write(row)
        l = read_file.readline()
    print '%s converted for ANNOVAR' % name

if len(sys.argv)!= 3:
    usage()
    sys.exit(2)

try:
    vcf_files = file(sys.argv[1],"r")
    name_file = open("./simulated_final_data/annovar_input.txt", "w")
    root = sys.argv[2]
    for name in vcf_files:
        #remove newline character at the end of each line
        convert(name[:-1], name_file, root)
    name_file.close()
    print 'ANNOVAR conversion complete.'

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)