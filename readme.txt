Readme.txt

John O’Leary and Sadiq Rehmani

1) Preface

Before we can begin to discuss the underlying mechanics of the myriad python and shell scripts included in this application, we first must take care of a few preparatory steps the user must take care of himself or herself. This involves downloading a few large databases from internet repositories (due to their size they were not included in this package), sample exome sequencing from the NHLBI Exome Sequencing Project website, and the ANNOVAR application.

The database files needed for this particular version are as follows:

The COSMIC database, which can be downloaded at: http://cancer.sanger.ac.uk/cancergenome/projects/cosmic/download (download ‘Complete COSMIC data’) 

The DBSNP database, which can be downloaded at: http://www.broadinstitute.org/cancer/cga/mutect_download (download dbsnp_132_b37.leftAligned.vcf.gz). NOTE: The user will have to login to the Broad Institute website to access this file. That being said, it is not difficult to obtain login credentials. One simply needs to fill out the application form on the main page.

After downloading these files and unzipping the DBSNP file, the user should rename them “Cosmic_database.txt” and “dbsnp_132_b37.leftAligned.txt.” After doing so, move the two downloaded files into the directory called “dbs.” The user can then run the python script “filter_dbsnp.py,” located in the directory “python_files” as follows:

python ./python_files/filter_dbsnp.py ./dbs/dbsnp_132_b37.leftAligned.txt

This will prune the DBSNP file to a much smaller size for system convenience.

Hopefully, in future versions, more db filtering will available for the user. In these expansions, all other database files (OMIM etc.) will be placed inside the dbs folder as well. Scripts similar to filter_dbsnp.py will be provided in these future editions.

After downloading and processing the database files, the user will have to provide his or her own tumor reads for the application to analyze. These VCF files should be placed in the directory called “init_data” and named using the following format:

“Tumor_X.vcf” where X is replaced with a unique identifier for each tumor file (e.g. 001, 002…). The names of all of these files should also be recorded in a newline delimited text file named “tumor_file_names.txt” in the manner shown in the sample provided.

Finally, the user can download ANNOVAR and the exome sequencing at the following locations:

ANNOVAR: http://www.openbioinformatics.org/annovar/annovar_download.html#main
exome sequencing: http://evs.gs.washington.edu/EVS/ (download ESP6500SI-V2-SSA137.protein-hgvs-update.snps_indels.vcf.tar.gz)

Be sure to move these files into the folder called ‘Downloaded_files.’ The unzipped exome sequencing directory should be called ‘ESP6500SI-V2-SSA137.protein-hgvs-update.snps_indels.vcf’. 

2) Running the main application

Three shell scripts have been provided for the user’s convenience. They are:

./map_mutations.sh
./gen_sample_data.sh
./analyze_sample_data.sh

map_mutations.sh is the central driver for this application, as it is the script that will generate the pathway counts for the tumor information. gen_sample_data.sh and analyze_sample_data.sh are provided as convenient tools for the user to generate his or her own benchmark information against which the tumor data can be compared.

If all of the steps outlined in part (1) of the readme are followed, the user needs only give execute permission to map_mutations.sh and run the command ./map_mutations.sh from the command line in order to produce the relevant pathway analysis. That being said, if it is the user’s first time running this application, the user must slightly modify the script. Line 21 of the script should be uncommented on the first run of the script, as it will download a database that is necessary for ANNOVAR to run properly. On future runs, line 21 can be commented out to save time and avoid redundancy (assuming the database is not deleted between runs).

gen_sample_data.sh and  ./analyze_sample_data.sh are also set up to be able to run without any additional arguments, but the user can modify those two shell scripts depending on how many simulated patient exome sequences he or she wants to use to produce baseline data. If the user wishes to change the number of simulate patients use, he or she needs only open the two scripts and modify the following lines:

In gen_sample data.sh: the last argument provided in line 12 should be the number of patients desired

In analyze_sample_data.sh: the last argument in line 52 should be the same number used in line 12 of gen_sample data.sh.

The end product of both map_mutations.sh and analyze_sample_data.sh will be written to the same directory (which is cleared upon each execution of one of these two shell scripts — so move analyses to another location if you want to save them!). That directory is ‘pathways.’ The user will note that the pathway analyses will further be subdivided into the subdirectories ‘biocarta,’ ‘kegg,’ ‘pid,’ and ‘reactome.’

map_mutations.sh will produce a pathway analysis for each tumor file with the corresponding unique tumor id in the file name. analyze_sample_data.sh will produce a single pathway analysis for each database that contains the average number of times a given pathway was activated across all simulated patient exome sequences. 

3) Python scripts

Though the python files are all commented, a brief overview of what each file does may be instructive. 

aggregate_vcf.py: This file compiles all of the exome sequences downloaded from the NHLBI Exome Sequencing Project website into a single vcf file. 

filter_dbsnp.py: This file will whittle down the DBSNP database to a much smaller file size. Once this is done, the original DBSNP file is no longer needed. 

filter_omim.py: Though the OMIM database is not used in this early version of the application, this is an example script of how one could once again pare down the large OMIM database file into something more manageable to read into memory.

filter_vcf.py: This is the initial filtration script for VCF files entering pathway analysis. The user will note the major filtration criterion, found in lines 23-30, has been commented out. This is due to the fact that the tumor data and simulated data used in the initial study did not have any useful “PASS” information that could be used in this step to evaluate read quality. In future runs, this may be more useful and can be uncommented by the user.

find_average_pathways.py: This will generate four total files, one for each targeted pathway database, that will provide the average number of activations a given pathway had over the baseline exome sequences as well as the standard deviation between sequences.

find_pathways.py: This will generate four pathway analysis files for each tumor VCF, one for each of the targeted pathway databases.

fold_back_checks.py: This merges the spliced files that are initially separated in query_dbsnp.py (see relevant entry), making sure that the finished product remains an ordered list.

query_cosmic.py: This checks the reads in a VCF file that showed up in the DBSNP against COSMIC. If they show up in COSMIC, they are folded back in with the non-DBSNP reads as potentially interesting mutations.

query_dbsnp.py: This checks whether the reads in a VCF file show up in the DBSNP and subdivides the input VCF file into two output VCF files: those reads that show up in DBSNP and those reads that do not.

simulate_data.py: This generates an arbitrary number of simulated exome sequences for the creation of baseline data to compare against the tumor data.