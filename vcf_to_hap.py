# Simple script to extract the values from all the samples of a given .VCF file, assign them an id and store in a .hap file
import sys
import pysam

def get_homozygosity(list):
    return (list[0] ** 2 + list[1] ** 2) / (sum(list) ** 2)

# Input VCF and output hap file paths and window size (as in SNP count)
def vcf_to_custom_haplo(vcf_path, hap_path, map_path, window_size):
    window_size = int(window_size)
    vcf = pysam.VariantFile(vcf_path)

    # dictionary to store samples
    sample_records = {}
    
    # dictionary to store MAF
    mafs = {}
    
    # dictionary to store MAF
    hzgys = {}

    # Iterate through VCF records
    for record in vcf:
        sample_maf = [0, 0]
        # Iterate through samples
        for sample in record.samples:
            sample_name = sample
            sample_values = record.samples[sample]["GT"]
            sample_maf[record.samples[sample]["GT"][0]] += 1
            sample_maf[record.samples[sample]["GT"][1]] += 1  
            # print(sample_values)

            if sample_name not in sample_records:
                sample_records[sample_name] = []

            sample_records[sample_name].append(sample_values)
            
            minor_allele_freq = min(sample_maf) / sum(sample_maf)
            mafs[record.id] = minor_allele_freq
            
            homozygosity = get_homozygosity(sample_maf)
            hzgys[record.id] = homozygosity

    vcf.close()

    print(f"#samples = {len(sample_records)}")
    # print(sample_records.keys())
    # print(f'{list(sample_records.keys())[0]}: {list(sample_records.values())[0]}')

    samples = {}

    # dictionary to store counts
    string_ids = {}
    id1 = 1  # for individual haplotypes
    id2 = 1  # for combined haplotypes i.e. diplotype

    with open(hap_path, "w") as file:
        i = 1
        for key, value in sample_records.items():
            str1 = []
            str2 = []

            for v in value:
                str1.append(str(v[0] + 1))
                str2.append(str(v[1] + 1))

            str1 = "".join(str1)
            str2 = "".join(str2)

            samples[key] = [str1, str2]

            substr1 = str1[:window_size]
            substr2 = str2[:window_size]
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
    print(f".hap output written to {hap_path}")
    
    with open(map_path, "w") as file:
        i = 0
        for key in mafs.keys():
            if i == window_size:
                break
            file.write(f"{key}\t{mafs[key]}\t{hzgys[key]}\n")
            i += 1
    print(f".map output written to {map_path}")
        


if __name__ == "__main__":
    vcf_to_custom_haplo(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
