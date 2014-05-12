#!/bin/bash
#clear out all files from previous runs if they exist
rm ./cosmic_queries/*
rm ./final_vcfs/*
rm ./gene_annotated/*
rm ./nondbsnp_vcfs/*
rm ./passed_vcfs/*
rm ./pathways/*
rm ./pathways/biocarta/*
rm ./pathways/kegg/*
rm ./pathways/pid/*
rm ./pathways/reactome/*
rm ./tocosmic_vcfs/*

python ./python_files/filter_vcf.py ./init_data/tumor_file_names.txt ./init_data/
python ./python_files/query_dbsnp.py ./passed_vcfs/passed_vcf_names.txt ./dbs/pruned_dbsnp.txt
python ./python_files/query_cosmic.py ./tocosmic_vcfs/tocosmic_vcf_names.txt ./dbs/Cosmic_database.txt
python ./python_files/fold_back_checks.py ./cosmic_queries/cosmic_query_names.txt ./nondbsnp_vcfs/nondbsnp_vcf_names.txt

#Use this command to download the humandb files needed for ANNOVAR annotation if you do not already have them.
perl ./Downloaded_files/annovar/annotate_variation.pl -buildver hg19 -downdb -webfrom annovar refGene humandb/


FILE="./final_vcfs/final_vcf_names.txt"
GENE_INDEX="./gene_annotated/gene_annotated_names.txt"
while read line
do
    OLD_FILE="./final_vcfs/$line"
    NAME_LEN=${#line}
    ROOT_NAME=${line:0:NAME_LEN-4}
    NEW_NAME="./gene_annotated/$ROOT_NAME.vcf4"
    echo "$ROOT_NAME.vcf4">>$GENE_INDEX
    perl ./Downloaded_files/annovar/convert2annovar.pl -format vcf4 $OLD_FILE -outfile $NEW_NAME
done < $FILE
FILE="./gene_annotated/gene_annotated_names.txt"
VAR_FUNC_INDEX="./gene_annotated/var_func_names.txt"
while read line
do
    OLD_FILE="./gene_annotated/$line"
    NAME_LEN=${#line}
    ROOT_NAME=${line:0:NAME_LEN-4}
    NEW_NAME="./pathways/$ROOT_NAME.vcf4"
    echo "$line.variant_function">>$VAR_FUNC_INDEX
    perl ./Downloaded_files/annovar/annotate_variation.pl -geneanno $OLD_FILE -buildver hg19 humandb/
done < $FILE
python ./python_files/find_pathways.py ./Downloaded_files/c2.all.v4.0.symbols.gmt ./simulated_pathway_data/pathway_names.txt ./gene_annotated/var_func_names.txt