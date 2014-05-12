#! /usr/bin/python
import sys
import csv

# filter_vcf.py
#
# This is a function that will grow in utility as our access to information
# improves. For the time being, it simply copies the information passed into
# it in another directory, passing it along for the next function call in the
# shell script. However, once PASS criteria (as well as our other proposed
# improvements) become more reliable, there will be an actual filtration process
# occuring in this file.

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 26, 2014"

def usage():
    print """
        python filter_vcf.py [tumor_file_names.txt] [file root]
        """

def filter(name, name_file, root):
    path = '%s%s' % (root, name)
    vcf_file = file(path, "r")
    write_file_name = './passed_vcfs/%s_passed.vcf' % (name[:-4])
    f = open(write_file_name, "w")
    #get rid of path from file names
    name_file.write('%s\n' % write_file_name[14:])
    l = vcf_file.readline()
    while l:
        f.write(l)
        #the commented out if/else statement is to be used if the vcf files are generated with 'PASS' filter criteria. since we didn't have that information for the tumor vcf files tested, we just skipped this step.
        
        #if l[0] == '#':
        #f.write(l)
        #else:
        #parts = l.split('\t')
        #f.write('%s\t%s\t%s\t%s\t%s\t.\t.\t%s\t%s\t.\n' % (parts[0],parts[1],parts[2],parts[3],parts[4],parts[7],parts[8]))
            #if parts[6] == 'PASS':
                #f.write(l)
        l = vcf_file.readline()
    f.close()
    print '%s filtered' % name

if len(sys.argv)!= 3:
    usage()
    sys.exit(2)

try:
    vcf_files = file(sys.argv[1],"r")
    name_file = open("./passed_vcfs/passed_vcf_names.txt", "w")
    root = sys.argv[2]
    for name in vcf_files:
        #remove newline character at the end of each line
        filter(name[:-1], name_file, root)
    name_file.close()
    print 'Initial VCF filtration complete.'

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)