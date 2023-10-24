# Simple script to extract the values from all the samples of a given .VCF file, assign them an id and store in a .hap file
import util
import json
import sys
    
# Input VCF and output hap file paths and window size (as in SNP count)
def vcf_to_custom_haplo(window_size, starting_window_number):
    window_size = int(window_size)
    starting_window_number = int(starting_window_number)
        
    with open('ds_info.json', 'r') as fp:
        ds_info = json.load(fp)
    with open('sample_genotypes.json', 'r') as fp:
        sample_genotypes = json.load(fp)
    with open('positions.json', 'r') as fp:
        positions = json.load(fp)
    with open('mafs.json', 'r') as fp:
        mafs = json.load(fp)
    with open('hzgys.json', 'r') as fp:
        hzgys = json.load(fp)
        
    dataset = ds_info['dataset']
    chromosome = ds_info['chromosome']
    
    #print(len(sample_genotypes), len(positions), len(hzgys))
    if len(positions) == len(hzgys):
        print("Iterating through records...pushing window by 1 SNP")
    else:
        print("Number of records mismatch")
        return exit(1)
    
    # If we want only the .hap and .map for a specific window (useful if running in parallel)
    # -1 for running all windows i.e. sequentially
    # if starting_window_number != -1:
    hap_path = f"{dataset}.{chromosome}.{starting_window_number}.hap"
    map_path = f"{dataset}.{chromosome}.{starting_window_number}.map"
    _ = util.get_HAP(hap_path, sample_genotypes, window_size, int(starting_window_number)-1)
    util.get_MAP(map_path, positions, hzgys, window_size, int(starting_window_number)-1)
    print(f"Generated .hap and .map for window {starting_window_number}")
    return exit(0)
    
    # for i in range(len(positions) - window_size + 1):
    #     hap_path = f"{dataset}.{chromosome}.{i+1}.hap"
    #     map_path = f"{dataset}.{chromosome}.{i+1}.map"
    #     _ = util.get_HAP(hap_path, sample_genotypes, window_size, i)
    #     util.get_MAP(map_path, positions, hzgys, window_size, i)
    #     print(f"Generated .hap and .map for window {i+1}")
    
if __name__ == "__main__":
    vcf_to_custom_haplo(sys.argv[1], sys.argv[2])
