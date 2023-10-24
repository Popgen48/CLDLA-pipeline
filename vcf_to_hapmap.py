# Simple script to extract the values from all the samples of a given .VCF file, assign them an id and store in a .hap file
import sys
import util
import os

# Input VCF and output hap file paths and window size (as in SNP count)
def vcf_to_custom_haplo(arg_list):
    vcf_path = str(arg_list[0])
    window_size = int(arg_list[1])
    window_number = int(arg_list[2])
    
    dataset = vcf_path.split('.')[0]
    chromosome = vcf_path.split('.')[1]

    sample_genotypes, positions, mafs, hzgys = util.read_vcf(vcf_path, window_size, window_number-1)
    
    if len(positions) != len(hzgys):
        print('Number of records mismatch')
        return exit(1) 
    
    if not os.path.exists(f'./{dataset}/{chromosome}'):
        os.makedirs(f'./{dataset}/{chromosome}')

    hap_path = f'./{dataset}/{chromosome}/{dataset}.{chromosome}.{window_number}.hap'
    map_path = f'./{dataset}/{chromosome}/{dataset}.{chromosome}.{window_number}.map'
    
    _ = util.get_HAP(hap_path, sample_genotypes)
    util.get_MAP(map_path, positions, hzgys)
    
    print(f'Generated .hap and .map for window {window_number+1}')
