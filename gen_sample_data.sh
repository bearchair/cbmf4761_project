#!/bin/bash

#  gen_sample_data.sh
#
#
#  Created by John O'Leary on 5/9/14.
#

rm ./simulated_init_data/*

python ./python_files/aggregate_vcf.py ./Downloaded_files/ESP6500SI-V2-SSA137.protein-hgvs-update.snps_indels.vcf
python ./python_files/simulate_data.py ./simulated_init_data/agg_vcf_template.vcf 2