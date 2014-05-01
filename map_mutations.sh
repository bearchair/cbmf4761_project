#!/bin/bash

python filter_vcf.py 2_Mutation_Report1.txt
python query_dbsnp.py init_vcf.txt pruned_dbsnp.txt
python query_cosmic.py test_further_vcf.txt Cosmic_database.txt
python fold_back_checks.py cosmic_queries.txt init_vcf.txt