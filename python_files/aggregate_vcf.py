#! /usr/bin/python
import sys
import os

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$May 9, 2014"

def usage():
    print """
        python aggregate_vcf.py [vcf_directory]
        """

def aggregate(directory_name):
    chr_number = 1
    agg_file = open("./simulated_init_data/agg_vcf_template.vcf", "w")
    while chr_number <= 22:
        file_name = 'ESP6500SI-V2-SSA137.updatedProteinHgvs.chr%s.snps_indels.vcf' % chr_number
        if chr_number == 1:
            process_file(directory_name, file_name, agg_file, 'y')
        else:
            process_file(directory_name, file_name, agg_file, 'n')
        chr_number = chr_number + 1

    file_name = 'ESP6500SI-V2-SSA137.updatedProteinHgvs.chrY.snps_indels.vcf'
    process_file(directory_name, file_name, agg_file, 'n')
    file_name = 'ESP6500SI-V2-SSA137.updatedProteinHgvs.chrX.snps_indels.vcf'
    process_file(directory_name, file_name, agg_file, 'n')

def process_file(directory_name, file_name, agg_file, is_first):
    path = '%s/%s' % (directory_name, file_name)
    vcf_file = file(path, "r")
    l = vcf_file.readline()
    while l:
        if l[0] == '#':
            if is_first == 'y':
                #filter out KeggPathwayIDs and GenesInThisRegion headers to save memory. I figure this is ok because we're dealing with simulated data anyway
                if l[2] != 'G' and l[2] != 'K':
                    agg_file.write(l)
            l = vcf_file.readline()
        else:
            parts = l.split('\t')
            #we have to put this in samtools format
            parts[0] = 'chr%s' % parts[0]
            #I'm once again removing the INFO portion to save space, as it is no longer valid anyway
            #parts [7] = '.'
            agg_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (parts[0],parts[1],parts[2],parts[3],parts[4],parts[5],parts[6], parts[7]))
            l = vcf_file.readline()

if len(sys.argv)!= 2:
    usage()
    sys.exit(2)

try:
    path = sys.argv[1]
    aggregate(path)
    print 'All vcf files in %s aggregated.' % sys.argv[1]

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)