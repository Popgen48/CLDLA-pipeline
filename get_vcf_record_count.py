import pysam
import sys
import os
import util

vcf_file_path = sys.argv[1]
chrom = sys.argv[2]
window_size = int(sys.argv[3])

vcf_file = pysam.VariantFile(vcf_file_path, 'r')

count = 0
for record in vcf_file:
    maf = util.get_maf(record)
    if maf[0] != 0 and maf[1] != 0:
        count += 1

vcf_file.close()

window_count = count - window_size + 1

output_file_path = chrom+'_window_counts.txt'

# check if file already exists
if not os.path.exists(output_file_path):
    with open(output_file_path, 'w') as output_file:
        for n_window in range(1,window_count+1):
            output_file.write(f"{chrom} {n_window}\n")

print(f'window count saved to {output_file_path}')
