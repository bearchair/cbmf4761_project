#! /usr/bin/python
import sys
import csv
from operator import itemgetter
from collections import defaultdict

# find_pathways.py
#
# This function handles pathway analysis for a tumor data. It first
# counts the number of times a pathway is activated in a given file of
# tumor reads and then compares it against baseline population statistics
# provided by the user. If the pathway seems to appear an unusually high
# or low number of times (defined here as outside of one standard deviation
# from the mean), it appears in a ranked list of unusual pathways, which are
# seperated by database.

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$May 3, 2014"

#this dictionary is indexed by gene name and will pull up a list of all associated pathways for the index value
pathway_dict = defaultdict(list)
#this list will store the final score for each pathway along with pathway name
distribution_info = defaultdict(list)

def usage():
    print """
        python find_pathways.py [c2.all.v4.0.orig.gmt] [simulated_pathway_data/pathway_names.txt] [file_name.variant_function]
        """

#this function simply reads our pathway databases into memory. One is the one we downloaded from the internet, the other is the database of baseline population statistics we will use to score our counts.
def load_pathway(pathway_db, normal_data):
    #first load gene association information for pathways
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

    #then load the non-cancerous reference data for pathways
    path = './simulated_pathway_data/'
    for line in normal_data:
        name = line[:-1]
        file_name = '%s%s' % (path, name)
        data = file(file_name, "r")
        l = data.readline()
        while l:
            parts = l.split('\t')
            distribution_info[parts[0]] = [float(parts[1]), float(parts[2][:-1])]
            l = data.readline()

    print 'Pathway data loaded into memory.'

#this function counts the number of pathway activations that occur for each pathway in file
def count_pathways(name, pathway_counts):
    
    #this will track the total number of pathways counted. this will enable us to find a ratio of observations of a given pathway to the total number of pathways, which can be compared with our simulated data
    total_count = 0
    
    #this is the file which has data to extract
    root = './gene_annotated/'
    path = '%s%s' % (root, name)
    gene_info = file(path, "r")

    #count
    l = gene_info.readline()
    while l:
        parts = l.split('\t')
        gene_name = parts[1]
        # we will ignore the off-chance that a gene name does not appear in the pathway database. this seems highly unlikely.
        if gene_name in pathway_dict:
            #this iterate through all pathways associated with a given gene name
            for entry in pathway_dict[gene_name]:
                #if the pathway has already been seen before, increment its counter by one
                if entry in pathway_counts:
                    pathway_counts[entry] = pathway_counts[entry] + 1
                    total_count = total_count +1
                #otherwise add an entry to the dictionary for the pathway
                else:
                    pathway_counts[entry] = 1
                    total_count = total_count +1
        l = gene_info.readline()

    return total_count, pathway_counts

#this function generates the score for each pathway activated in the file
def score_pathways(total_count, pathway_counts):
    scored_pathways = []
    rare_pathway_counts = 0
    
    for pathway in pathway_counts:
        ratio = float(pathway_counts[pathway])/float(total_count)
        #as we may have pathways that do not appear in our non-cancer reads
        if pathway in distribution_info:
            #if a pathway has appeared outside of one standard deviation of the expected number of times for the non-cancer simulated data, include it. for a score, we will use the observed pathways distance from the boundary of the 95% confidence interval
            
            #if we have a below average number of activations for a pathway
            if ratio < (distribution_info[pathway][0] - distribution_info[pathway][1]):
                boundary = distribution_info[pathway][0] - distribution_info[pathway][1]
                distance = boundary - ratio
                temp = [pathway, distance]
                scored_pathways.append(temp)
            #if we have an above average number of activations for a pathway
            elif ratio > (distribution_info[pathway][0] + distribution_info[pathway][1]):
                boundary = distribution_info[pathway][0] + distribution_info[pathway][1]
                distance = ratio - boundary
                temp = [pathway, distance]
                scored_pathways.append(temp)
    
        #we have to handle rare reads seperately. For the time being, rare reads will have precedence over other reads. It doesn't seem any of the pathways in the databases we are consulting are unlisted in our pathway database.
        else:
            score = 1
            temp = [pathway, score]
            scored_pathways.append(temp)
            rare_pathway_counts = rare_pathway_counts + 1
    
    print '%s rare pathways found.' % rare_pathway_counts
    return scored_pathways

#this function writes the relevent pathways and their associated scores to memory
def print_pathways(name, name_file, pathway_scores):
    
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

    for x in sorted(pathway_scores, key = itemgetter(1), reverse = True):
        if 'KEGG' in x[0]:
            KEGG_file.write('%s\t%s\n' % (x[0], x[1]))
        elif 'BIOCARTA' in x[0]:
            BIOCARTA_file.write('%s\t%s\n' % (x[0], x[1]))
        elif 'REACTOME' in x[0]:
            REACTOME_file.write('%s\t%s\n' % (x[0], x[1]))
        elif 'PID' in x[0]:
            PID_file.write('%s\t%s\n' % (x[0], x[1]))
    KEGG_file.close()
    BIOCARTA_file.close()
    REACTOME_file.close()
    PID_file.close()

if len(sys.argv)!= 4:
    usage()
    sys.exit(2)

try:
    pathway_db = file(sys.argv[1],"r")
    normal_data = file(sys.argv[2], "r")
    file_names = file(sys.argv[3],"r")
    name_file = open("./pathways/pathway_names.txt", "w")
    load_pathway(pathway_db, normal_data)
    print 'Pathway information loaded.'
    for name in file_names:
        #this dictionary is indexed by pathway name and stores the number of times a pathway appears in a given tumor file
        pathway_counts = defaultdict(int)
        #remove newline character at the end of each line
        total_count, pathway_counts = count_pathways(name[:-1], pathway_counts)
        pathway_scores = score_pathways(total_count, pathway_counts)
        print_pathways(name[:-1], name_file, pathway_scores)
    name_file.close()
    print 'All pathway information calculated.'

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)