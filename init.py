# Call only once, stores the necessary information into a .json file to be used for further procesing.

import util
import json

def initialize(vcf_path):
    dataset = vcf_path.split(".")[0]
    chromosome = vcf_path.split(".")[1]
    
    ds_info = {'dataset': dataset, 'chromosome': chromosome}
    
    with open('ds_info.json', 'w') as fp:
        json.dump(ds_info, fp)

    sample_genotypes, positions, mafs, hzgys = util.read_vcf(vcf_path)
    
    with open('sample_genotypes.json', 'w') as fp:
        json.dump(sample_genotypes, fp)
    print(f'sample_genotypes.json written to file')
    
    with open('positions.json', 'w') as fp:
        json.dump(positions, fp)
    print(f'positions.json written to file')
    
    with open('mafs.json', 'w') as fp:
        json.dump(mafs, fp)
    print(f'mafs.json written to file')
    
    with open('hzgys.json', 'w') as fp:
        json.dump(hzgys, fp)
    print(f'hzgys.json written to file')
    
    
    