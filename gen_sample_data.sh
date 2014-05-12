#!/bin/bash

#  gen_sample_data.sh
#
#
#  Created by John O'Leary on 5/9/14.
#

rm ./cosmic_queries/*
rm ./final_vcfs/*
rm ./gene_annotated/*
rm ./nondbsnp_vcfs/*
rm ./passed_vcfs/*
rm ./tocosmic_vcfs/*
rm ./simulated_init_data/*
rm ./simulated_final_data/*

python ./python_files/aggregate_vcf.py ./Downloaded_files/ESP6500SI-V2-SSA137.protein-hgvs-update.snps_indels.vcf
python ./python_files/simulate_data.py ./simulated_init_data/agg_vcf_template.vcf 2
python ./python_files/filter_vcf.py ./simulated_init_data/simulated_data.txt ./simulated_init_data/
python ./python_files/query_dbsnp.py ./passed_vcfs/passed_vcf_names.txt ./dbs/pruned_dbsnp.txt
python ./python_files/query_cosmic.py ./tocosmic_vcfs/tocosmic_vcf_names.txt ./dbs/Cosmic_database.txt
python ./python_files/fold_back_checks.py ./cosmic_queries/cosmic_query_names.txt ./nondbsnp_vcfs/nondbsnp_vcf_names.txt
python ./python_files/convert_to_annovar_input.py ./final_vcfs/final_vcf_names.txt ./final_vcfs/

#Use this command to download the humandb files needed for ANNOVAR annotation if you do not already have them.
#perl ./Downloaded_files/annovar/annotate_variation.pl -buildver hg19 -downdb -webfrom annovar refGene humandb/

FILE="./simulated_final_data/annovar_input.txt"
VAR_FUNC_INDEX="./simulated_final_data/var_func_names.txt"
while read line
do
OLD_FILE="./simulated_final_data/$line"
NAME_LEN=${#line}
ROOT_NAME=${line:0:NAME_LEN-4}
NEW_NAME="./pathways/$ROOT_NAME.vcf4"
echo "$line.variant_function">>$VAR_FUNC_INDEX
perl ./Downloaded_files/annovar/annotate_variation.pl -geneanno $OLD_FILE -buildver hg19 humandb/
done < $FILE