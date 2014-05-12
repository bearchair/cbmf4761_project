#! /usr/bin/python
import sys
import os
import random

# simulate_data.py
#
# This function simulates single nucleotide mutations across non-cancerous full exome reads.
# It does so independently and pseudorandomly.

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$May 9, 2014"

def usage():
    print """
        python simulate_data.py [template.vcf] [number of simulated patients]
        """

#this function will generate a user-determined number of simulated data files
def simulate(template, patient_count):
    genotypes = ['A', 'C', 'G', 'T']
    path = './simulated_init_data/'
    files = []
    count = 1
    name_file_name = '%ssimulated_data.txt' % path
    name_file = open(name_file_name, "w")
    
    #open files
    while count <= patient_count:
        if count < 10:
            file_name = 'patient_0%s.vcf' % count
            full_name = '%s%s' % (path, file_name)
            temp = open(full_name, "w")
            files.append(temp)
            name_file.write('%s\n' % file_name)
        else:
            file_name = 'patient_%s.vcf' % count
            full_name = '%s%s' % (path, file_name)
            temp = open(full_name, "w")
            files.append(temp)
            name_file.write('%s\n' % file_name)
        count = count + 1

    l = template.readline()
    while l:
        if l[0] == '#':
            for file in files:
                file.write(l)
        else:
            for file in files:
                genotype_index = random.randint(0,3)
                parts = l.split('\t')
                #if we randomly pick a variant allele that is the same as the reference allele, we should not include it in our file
                if parts[3] != genotypes[genotype_index]:
                #if we randomly pick same variant allele as it appeared in our template, just write the whole line into the file (which allows us to preserve rsid)
                    if parts[4] == genotypes[genotype_index]:
                        file.write(l)
                #otherwise overwrite rsid and variant allele spots and then write in line
                    else:
                        parts[2] = '.'
                        parts[4] = genotypes[genotype_index]
                        file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (parts[0],parts[1],parts[2],parts[3],parts[4],parts[5],parts[6],parts[7]))

        l = template.readline()
    #write header in each file


if len(sys.argv)!= 3:
    usage()
    sys.exit(2)

try:
    template = open(sys.argv[1], "r")
    patient_count = int(sys.argv[2])
    simulate(template, patient_count)
    print 'All patient data simulated.'

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)