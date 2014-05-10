#! /usr/bin/python
import sys
import csv
import operator
from collections import defaultdict

pathway_dict = defaultdict(list)
pathway_counts = defaultdict(float)

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$May 10, 2014"

def usage():
    print """
        python find_average_pathways.py [c2.all.v4.0.orig.gmt] [file_name.variant_function] [total file count]
        """

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

def count_pathways(name):
    
    #this is the file which has data to extract
    root = './gene_annotated/'
    path = '%s%s' % (root, name)
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
                else:
                    pathway_counts[entry] = 1
        l = gene_info.readline()

def print_pathways(name, name_file):
    
    #write to name_file
    name_parts = name.split('_')
    tumor_name = '%s_%s' % (name_parts[0], name_parts[1])

    KEGG_name = './pathways/kegg/%s_KEGG_pathways.txt' % tumor_name
    KEGG_file = open(KEGG_name, "w")
    BIOCARTA_name = './pathways/biocarta/%s_BIOCARTA_pathways.txt' % tumor_name
    BIOCARTA_file = open(BIOCARTA_name, "w")
    REACTOME_name = './pathways/reactome/%s_REACTOME_pathways.txt' % tumor_name
    REACTOME_file = open(REACTOME_name, "w")
    PID_name = './pathways/pid/%s_PID_pathways.txt' % tumor_name
    PID_file = open(PID_name, "w")
    name_file.write('%s_BIOCARTA_pathways.txt\n' % tumor_name)
    name_file.write('%s_KEGG_pathways.txt\n' % tumor_name)
    name_file.write('%s_PID_pathways.txt\n' % tumor_name)
    name_file.write('%s_REACTOME_pathways.txt\n' % tumor_name)

    for x in sorted(pathway_counts, key = pathway_counts.get, reverse = True):
        parts = x.split('_')
        if parts[0] == 'KEGG':
            KEGG_file.write('%s\t%s\n' % (x, pathway_counts[x]))
        elif parts[0] == 'BIOCARTA':
            BIOCARTA_file.write('%s\t%s\n' % (x, pathway_counts[x]))
        elif parts[0] == 'REACTOME':
            REACTOME_file.write('%s\t%s\n' % (x, pathway_counts[x]))
        elif parts[0] == 'PID':
            PID_file.write('%s\t%s\n' % (x, pathway_counts[x]))
    KEGG_file.close()
    BIOCARTA_file.close()
    REACTOME_file.close()
    PID_file.close()

def average_pathway_count(patient_count):
    for entry in pathway_counts:
        pathway_counts[entry] = pathway_counts[entry]/patient_count


if len(sys.argv)!= 4:
    usage()
    sys.exit(2)

try:
    pathway_db = file(sys.argv[1],"r")
    file_names = file(sys.argv[2],"r")
    patient_count = float(sys.argv[3])
    name_file = open("./pathways/pathway_names.txt", "w")
    load_pathway(pathway_db)
    for name in file_names:
        #remove newline character at the end of each line
        count_pathways(name[:-1])
        print '%s pathway data counted.' % name
    average_pathway_count(patient_count)
    print 'Pathway information averaged.'
    print_pathways(name[:-1], name_file)
    name_file.close()
    print 'All pathway information calculated.'

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)