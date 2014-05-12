#! /usr/bin/python
import sys
import csv
from operator import itemgetter
import numpy
from collections import defaultdict
import random

# find_average_pathways.py
#
# This function handles the calculation of population statistics from
# the data simulated by our shell function. It takes in the gene annotated
# versions of our simulated data, pulls a subset of those files (specified
# by the user) some number of times (also specified by the user), and
# calculates population means and standard deviations that can be used in
# tumor pathway analysis. It is a comparatively large file due to its
# comparative complexity.

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$May 10, 2014"

#this dictionary is indexed by gene name and will pull up a list of all associated pathways for the index value
pathway_dict = defaultdict(list)
#this dictionary is indexed by pathway name and will store a list of ratios of the average number of times a pathway is activated divided by the total number of pathway activations in a file
sample_means = defaultdict(list)
#this list will store the population statistics for each pathway
distribution_info = []
#this rare_hits counter will be useful for future versions, when we include a more sophisticated way of handling the possibility of there being pathways activated in the tumor data that do not show up in our pathway database (one possible strategy is to tag all pathways that are activated under a certain threshold as 'RARE' and then generate population statistics for activating a 'RARE' pathway)
rare_hits = 0

def usage():
    print """
        python find_average_pathways.py [c2.all.v4.0.orig.gmt] [file_name.variant_function] [total file count] [sample size]
        """

#this function simply reads our pathway database into memory
def load_pathway(pathway_db):
    l = pathway_db.readline()
    while l:
        parts = l.split('\t')
        num_keys = len(parts)
        i = 2
        while i < num_keys:
            key = parts[i]
            entry = parts[0]
            if key in pathway_dict:
                if entry not in pathway_dict[key]:
                    pathway_dict[key].append(entry)
            else:
                pathway_dict[key] = [entry]
            i = i+1
        l = pathway_db.readline()
    print 'Pathway data loaded into memory.'

#this function counts the average number of pathway activations that occur for each pathway in a given sample
def count_pathways(samples):
    global sample_means
    total_hits = 0
    pathway_counts = defaultdict()
    sample_size = float(len(samples))
    
    #this is the file which has data to extract
    for sample in samples:
        root = './simulated_final_data/'
        path = '%s%s' % (root, sample)
        gene_info = file(path, "r")
        #count
        l = gene_info.readline()
        while l:
            parts = l.split('\t')
            gene_name = parts[1]
            if gene_name in pathway_dict:
                for entry in pathway_dict[gene_name]:
                    if entry in pathway_counts:
                        pathway_counts[entry] = pathway_counts[entry] + 1
                        total_hits = total_hits + 1
                    else:
                        pathway_counts[entry] = 1
                        total_hits = total_hits + 1
            l = gene_info.readline()
    
    #once the initial counts are made, we can then calculate ratios
    for pathway in pathway_counts:
        if pathway in sample_means:
            #this first quotient is the total number of times a pathway is activated across all samples divided by the total number of pathway activations across all files
            x = pathway_counts[pathway]/total_hits
            #the second quotient is what the ratio should be in a single file
            sample_means[pathway].append(x/sample_size)
        else:
            temp = []
            x = pathway_counts[pathway]/total_hits
            temp.append(x/sample_size)
            sample_means[pathway] = temp

#this function writes the relevent population statistics to file
def print_pathways():
    
    global total_hits
    
    KEGG_name = './simulated_pathway_data/kegg/KEGG_pathway_data.txt'
    KEGG_file = open(KEGG_name, "w")
    print 'KEGG file opened'
    BIOCARTA_name = './simulated_pathway_data/biocarta/BIOCARTA_pathway_data.txt'
    BIOCARTA_file = open(BIOCARTA_name, "w")
    print 'BIOCARTA file opened'
    REACTOME_name = './simulated_pathway_data/reactome/REACTOME_pathway_data.txt'
    REACTOME_file = open(REACTOME_name, "w")
    print 'REACTOME file opened'
    PID_name = './simulated_pathway_data/pid/PID_pathway_data.txt'
    PID_file = open(PID_name, "w")
    print 'PID file opened'

    #sort distribution info descending, starting with largest mean count for pathway
    for x in sorted(distribution_info, key = itemgetter(1), reverse = True):
        parts = x[0].split('_')
        if parts[0] == 'KEGG':
            KEGG_file.write('%s\t%s\t%s\n' % (x[0], x[1], x[2]))
        elif parts[0] == 'BIOCARTA':
            BIOCARTA_file.write('%s\t%s\t%s\n' % (x[0], x[1], x[2]))
        elif parts[0] == 'REACTOME':
            REACTOME_file.write('%s\t%s\t%s\n' % (x[0], x[1], x[2]))
        elif parts[0] == 'PID':
            PID_file.write('%s\t%s\t%s\n' % (x[0], x[1], x[2]))
    KEGG_file.close()
    BIOCARTA_file.close()
    REACTOME_file.close()
    PID_file.close()

#this function writes data to the name file, it was written to remove clutter from the driver commands
def write_name_file(name_file):
    name_file.write('biocarta/BIOCARTA_pathway_data.txt\n')
    name_file.write('kegg/KEGG_pathway_data.txt\n')
    name_file.write('pid/PID_pathway_data.txt\n')
    name_file.write('reactome/REACTOME_pathway_data.txt\n')

#this function produces an array of file names picked pseudorandomly from our simulated exome sequences.
def choose_sample(samples, patient_count, sample_size):
    i = 0
    #sample_size is user defined
    while i < sample_size:
        #first choose which number files we will sample
        sample_num = random.randint(1, patient_count)
        #we need to add a zero to the front of any number less than 10 to satisfy file naming convention
        if sample_num < 10:
            sample_num = '0%s' % sample_num
        else:
            sample_num = str(sample_num)
        #be sure not to include duplicate files
        if sample_num not in samples:
            samples.append(sample_num)
            i = i+1

    #now write out the full file name
    z = 0
    while z < sample_size:
        samples[z] = 'patient_%s_final.human.variant_function' % samples[z]
        z = z+1

    return samples

#this function calls several other functions in order to carry out the purpose of find_average_pathways.py
def eval_samples(patient_count, sample_size):
    i = 0
    #this is an arbitrary number, a relatively low number was picked for initial testing due to the length of time it takes for this file to run
    while i < 5:
        samples = []
        samples = choose_sample(samples, patient_count, sample_size)
        count_pathways(samples)
        print 'Sample batch %s evaluated.' % (i+1)
        i = i+1

#this function calculates the final population mean and standard deviation for each pathway
def calc_distribution():
    global distribution_info
    #this pulls out an array that is pointed to by a pathway name
    for pathway in sample_means:
        #calculate population mean and standard deviation from the sampling distribution
        pop_mean = numpy.mean(sample_means[pathway])
        pop_std = numpy.std(sample_means[pathway])
        
        #add this information to the distribution_info dictionary
        temp = (pathway, pop_mean, pop_std)
        distribution_info.append(temp)

if len(sys.argv)!= 5:
    usage()
    sys.exit(2)

try:
    #read in arguments
    pathway_db = file(sys.argv[1],"r")
    file_names = file(sys.argv[2],"r")
    patient_count = float(sys.argv[3])
    sample_size = float(sys.argv[4])
    
    #write the names of the files that will hold the pathway analyses
    name_file = open("./simulated_pathway_data/pathway_names.txt", "w")
    write_name_file(name_file)
    
    #load pathway information
    load_pathway(pathway_db)
    print 'Pathway information loaded. Begin sampling and evaluation.'
    #evaluate samples of population
    eval_samples(patient_count, sample_size)
    print 'Sample evaluation done. Begin calculating the sample distributions.'
    calc_distribution()
    print 'Sample distributions calculated.'
    print_pathways()
    name_file.close()
    print 'All pathway tasks finished.'

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)