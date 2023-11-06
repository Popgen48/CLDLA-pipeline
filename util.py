import pysam

def get_homozygosity(list):
    return (list[0] ** 2 + list[1] ** 2) / (sum(list) ** 2)

def get_maf(record):
    mafs = [0, 0]
    for val in record.samples:
        if record.samples[val]['GT'][0] != None:
            mafs[record.samples[val]['GT'][0]] += 1
        if record.samples[val]['GT'][1] != None:
            mafs[record.samples[val]['GT'][1]] += 1
    return mafs

def read_vcf(vcf_path, window_size, window_number):
    sample_genotypes = {}   # dictionary to store sample genotypes
    mafs = {}               # dictionary to store MAF
    hzgys = {}              # dictionary to store homozygosity
    positions = {}          # dictionary to store positions

    vcf = pysam.VariantFile(vcf_path)

    # Iterate through VCF records
    for i, record in enumerate(vcf):
        if i < window_number:
            continue
        if i >= window_number + window_size:
            break
        
        # calculate maf only collect the genotypes if the maf is grt than 0
        maf = get_maf(record)
        
        if maf[0] != 0 and maf[1] != 0:
            # Iterate through samples
            for sample in record.samples:
                sample_values = record.samples[sample]['GT']
                if sample not in sample_genotypes:
                    sample_genotypes[sample] = []

                sample_genotypes[sample].append(sample_values)
                
            if not record.id:
                record.id = f'{record.chrom}_{record.pos}'
                
            # While maf is collected here, it is not used in downstream analysis
            mafs[record.id] = min(maf) / sum(maf)
            
            homozygosity = get_homozygosity(maf)
            hzgys[record.id] = homozygosity
            
            positions[record.id] = record.pos / 1e6
        else:
            i -= 1

    vcf.close()

    return sample_genotypes, positions, mafs, hzgys
    
def get_HAP(hap_path, sample_genotypes):
    samples = {}
    string_ids = {}     # dictionary to store counts
    id1 = 1             # for individual haplotypes
    id2 = 1             # for combined haplotypes i.e. diplotype

    with open(hap_path, 'w') as file:
        i = 1
        for key, value in sample_genotypes.items():
            str1 = []
            str2 = []
            for v in value:
                str1.append(str(v[0] + 1))
                str2.append(str(v[1] + 1))

            str1 = ''.join(str1)
            str2 = ''.join(str2)

            samples[key] = [str1, str2]

            combined_substr = str1 + str2
            combined_sbstr_rev = str2 + str1

            if str1 not in string_ids:
                string_ids[str1] = id1
                id1 += 1
            h1 = string_ids[str1]
            if str2 not in string_ids:
                string_ids[str2] = id1
                id1 += 1
            h2 = string_ids[str2]
            if combined_substr not in string_ids:
                if combined_sbstr_rev in string_ids:
                    combined_substr = combined_sbstr_rev
                else:
                    string_ids[combined_substr] = id2
                    id2 += 1
            d = string_ids[combined_substr]

            file.write(
                f'{i}\t{h1}\t{h2}\t{d}\t{str1}\t{str2}\n'
            )  # tab delimited for readability
            i += 1
    return len(samples)

def get_MAP(map_path, positions, hzgys):
    with open(map_path, 'w') as file:
        for key in hzgys.keys():
            file.write(f'{key}\t{positions[key]}\t{hzgys[key]}\n')
            
def get_PAR(par_path, window_size, window_number, n_samples):
    with open(par_path, 'w') as file:
        file.write(f'100\n100\n{window_size+1}\n{window_number+1 if window_number <= int(window_size/2) else int(window_size/2)+1}\n{n_samples}')
        
def compare(f1, f2): # f1 is test, f2 is truth
    identical = True
    with open(f1, 'r') as file1, open(f2, 'r') as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()
    
        # compare the lines of each file
        for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
            line1 = line1.strip().split()
            line2 = line2.strip().split()
            if f1.endswith(".hap"):
                hap = []
                for item in line1:
                    hap.extend((list(item)))
                line1 = hap
            if f1.endswith(".par"):
                line2 = line2[0]
            if line1 != line2:
                identical = False
                print(f"Files differ at line {i+1}:")
                print(f"File 1: {line1.strip()}")
                print(f"File 2: {line2.strip()}")
                print("-------------")
                #break
        if identical:
            print(f"Files {f1} and {f2} are identical")

