import pysam
import sys
import os

vcf_file_path = sys.argv[1]

vcf_file = pysam.VariantFile(vcf_file_path, 'r')

record_count = sum(1 for _ in vcf_file)

vcf_file.close()

output_file_path = 'record_counts.txt'

# check if file already exists
if not os.path.exists(output_file_path):
    with open(output_file_path, 'w') as output_file:
        output_file.write(f"{vcf_file_path}: {record_count}\n")
else:
    # check if the record count already exists
    with open(output_file_path, 'r') as output_file:
        line = output_file.readline()
        if line.split(':')[0].strip() == vcf_file_path:
            print(f'Record count for {vcf_file_path} already exists')
            exit(1)

    # add count if it does not exist
    with open(output_file_path, 'a') as output_file:
        output_file.write(f'{vcf_file_path}: {record_count}\n')

print(f'Record count saved to {output_file_path}')