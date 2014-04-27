#!/bin/bash

python filter_vcf.py 2_Mutation_Report1.txt
python filter_omim.py omim.txt
python query_cosmic.py filtered_vcf.txt Cosmic_database.txt