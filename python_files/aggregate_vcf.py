#! /usr/bin/python
import sys
import os

# aggregate_vcf.py
#
# This function combines all of the non-cancerous exome sequences, which are
# currently divided by chromosome, into a single VCF file. This VCF file will
# serve as a template for a simulated training data for developing baseline
# population statistics with which we can score our tumor pathway data.
#

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$May 9, 2014"

def usage():
    print """
        python aggregate_vcf.py [vcf_directory]
        """

#this function takes in a directory name and, one by one, reads in the data of all the files found in that directory and concatanetes their essential information into a single file
def aggregate(directory_name):
    chr_number = 1
    
    #this will be the file that contains the amalgamation of all the files we will be processing
    agg_file = open("./simulated_init_data/agg_vcf_template.vcf", "w")
    
    #this while loop handles all of the files for the 22 chromosomes identified by number
    while chr_number <= 22:
        file_name = 'ESP6500SI-V2-SSA137.updatedProteinHgvs.chr%s.snps_indels.vcf' % chr_number
        #if it is the first file we're reading in, you need to include a flag that indicates this to be the case
        if chr_number == 1:
            process_file(directory_name, file_name, agg_file, 'y')
        else:
            process_file(directory_name, file_name, agg_file, 'n')
        chr_number = chr_number + 1

    #It was simplest to just hardcode in two special cases to handle the Y and X chromosomes. I read Y in before X in order to preserve the hierarchy found in the original directory.
    file_name = 'ESP6500SI-V2-SSA137.updatedProteinHgvs.chrY.snps_indels.vcf'
    process_file(directory_name, file_name, agg_file, 'n')
    file_name = 'ESP6500SI-V2-SSA137.updatedProteinHgvs.chrX.snps_indels.vcf'
    process_file(directory_name, file_name, agg_file, 'n')

#this function handles the actual task of reading in an individual file and copying its relevant information into our aggregate file
def process_file(directory_name, file_name, agg_file, is_first):
    #we first open up the file that needs to be read
    path = '%s/%s' % (directory_name, file_name)
    vcf_file = file(path, "r")
    l = vcf_file.readline()
    header_count = 1
    #iterating through the file
    while l:
        #we first encounter the header of the VCF file (which contains the metadata etc)
        if l[0] == '#':
            #we only copy the header information once into our aggregate VCF template, as such we only pay attention to it if this is our first time through a VCF file
            if is_first == 'y':
                #filter out all non-essential headers to save space
                if header_count not in [3,4,6,8,9] and header_count < 12:
                    agg_file.write(l)
                header_count = header_count + 1
            l = vcf_file.readline()
        #having gone through the header files, we now move on to the actual read information, we need to copy parts of all remaining rows in the file
        else:
            parts = l.split('\t')
            #we have to put this in samtools format, which means we need the tag 'chr' to precede chromosome position (we maintain samtools vcf format in case we need to use a common VCF program in future editions)
            parts[0] = 'chr%s' % parts[0]
            #The 'INFO'
            info_parts = parts[7].split(';')
            parts[7] = '%s;%s;%s;%s;%s\n' % (info_parts[0],info_parts[3],info_parts[5],info_parts[8],info_parts[9])
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