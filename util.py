import pysam

def get_homozygosity(list):
    return (list[0] ** 2 + list[1] ** 2) / (sum(list) ** 2)

def get_maf(record):
    mafs = [0, 0]
    for val in record.samples:
        if record.samples[val]["GT"][0] != None:
            mafs[record.samples[val]["GT"][0]] += 1
        if record.samples[val]["GT"][1] != None:
            mafs[record.samples[val]["GT"][1]] += 1
    return mafs

def read_vcf(vcf_path):
    # dictionary to store sample genotypes
    sample_genotypes = {}
    # dictionary to store MAF
    mafs = {}
    # dictionary to store homozygosity
    hzgys = {}
    # dictionary to store positions
    positions = {}

    vcf = pysam.VariantFile(vcf_path)

    # Iterate through VCF records
    for record in vcf:
        # calculate maf only collect the genotypes if the maf is grt than 0
        maf = get_maf(record)
        
        if maf[0] != 0 and maf[1] != 0:
            # Iterate through samples
            for sample in record.samples:
                sample_values = record.samples[sample]["GT"]
                if sample not in sample_genotypes:
                    sample_genotypes[sample] = []

                sample_genotypes[sample].append(sample_values)
                
            
            if not record.id:
                record.id = f"{record.chrom}_{record.pos}"
            # While maf is collected here, it is not used in downstream analysis
            mafs[record.id] = min(maf) / sum(maf)
            
            homozygosity = get_homozygosity(maf)
            hzgys[record.id] = homozygosity
            
            positions[record.id] = record.pos / 1e6

    vcf.close()

    print(f"#valid samples = {len(sample_genotypes)}")
    return sample_genotypes, positions, mafs, hzgys

def get_HAP(hap_path, sample_genotypes, window_size, window_number):
    window_size = int(window_size)

    samples = {}

    # dictionary to store counts
    string_ids = {}
    id1 = 1  # for individual haplotypes
    id2 = 1  # for combined haplotypes i.e. diplotype

    with open(hap_path, "w") as file:
        i = 1
        for key, value in sample_genotypes.items():
            str1 = []
            str2 = []

            for v in value:
                str1.append(str(v[0] + 1))
                str2.append(str(v[1] + 1))

            str1 = "".join(str1)
            str2 = "".join(str2)

            samples[key] = [str1, str2]

            substr1 = str1[window_number:window_size+window_number]
            substr2 = str2[window_number:window_size+window_number]
            combined_substr = substr1 + substr2
            combined_sbstr_rev = substr2 + substr1

            if substr1 not in string_ids:
                string_ids[substr1] = id1
                id1 += 1
            h1 = string_ids[substr1]
            if substr2 not in string_ids:
                string_ids[substr2] = id1
                id1 += 1
            h2 = string_ids[substr2]
            if combined_substr not in string_ids:
                if combined_sbstr_rev in string_ids:
                    combined_substr = combined_sbstr_rev
                else:
                    string_ids[combined_substr] = id2
                    id2 += 1
            d = string_ids[combined_substr]

            file.write(
                f"{i}\t{d}\t{h1}\t{h2}\t{substr1}\t{substr2}\n"
            )  # tab delimited for readability
            i += 1
    #print(f".hap output written to {hap_path}")
    return samples

def get_MAP(map_path, positions, hzgys, window_size, window_number):
    with open(map_path, "w") as file:
        for key in list(hzgys.keys())[window_number:window_size+window_number]:
            file.write(f"{key}\t{positions[key]}\t{hzgys[key]}\n")
    #print(f".map output written to {map_path}")