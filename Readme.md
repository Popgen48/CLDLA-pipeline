Get the number of records of the vcf file: `python3 get_vcf_record_count.py {vcf_file_path}`

Run `python3 parallelize.py {vcf_file_path} {window_size} {n_processes}`

Output is saved under `./{dataset}/{chromosome}`

## For Bending using Rscript

Run `Rscript bend.R {input_file} {output_file} {method ([lrs]/hj)}`

Default method used here is 'lrs'. More about it at 'https://cran.r-project.org/web/packages/mbend/mbend.pdf'
