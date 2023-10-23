# Simple script to extract the values from all the samples of a given .VCF file, assign them an id and store in a .hap file
import sys
import pysam
<<<<<<< HEAD:noob2.py
import pandas
=======

window_size = 40
>>>>>>> origin/master:vcfToHap.py


# Input VCF and output hap file paths and window size (as in SNP count)
def vcf_to_custom_haplo(vcf_path, hap_path, window_size):
    window_size = int(window_size)
    vcf = pysam.VariantFile(vcf_path)

    # dictionary to store samples
    sample_records = {}

    # Iterate through VCF records
    for record in vcf:
        # Iterate through samples
        for sample in record.samples:
            sample_name = sample
            sample_values = record.samples[sample]["GT"]
            # print(sample_values)

            if sample_name not in sample_records:
                sample_records[sample_name] = []

            sample_records[sample_name].append(sample_values)

    vcf.close()

    print(f"#samples = {len(sample_records)}")
    # print(sample_records.keys())
    # print(f'{list(sample_records.keys())[0]}: {list(sample_records.values())[0]}')

    samples = {}

    # dictionary to store counts
    string_ids = {}
    id1 = 1  # for individual haplotypes
    id2 = 1  # for combined haplotypes i.e. diplotype

    df = pandas.DataFrame(
        columns=["sample_id", "combined_id", "id1", "id2", "haplotype1", "haplotype2"]
    )

<<<<<<< HEAD:noob2.py
    with open(hap_path + ".tsv", "w") as file:
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

            if substr1 not in string_ids:
                string_ids[substr1] = id1
                id1 += 1
            h1 = string_ids[substr1]
            if substr2 not in string_ids:
                string_ids[substr2] = id1
                id1 += 1
            h2 = string_ids[substr2]
            if combined_substr not in string_ids:
                string_ids[combined_substr] = id2
                id2 += 1
            d = string_ids[combined_substr]

            df.loc[i - 1] = [i, d, h1, h2, substr1, substr2]
            file.write(
                f"{i}\t{d}\t{h1}\t{h2}\t{substr1}\t{substr2}\n"
            )  # tab delimited for readability
            i += 1

    # print(f'{list(samples.keys())[0]}: {list(samples.values())[0]}')
    df.to_csv(
        hap_path + ".csv"
    )  # why cant be the output file name of the csv be the same as hap_path
    print(f"output wirten to {hap_path}")


if __name__ == "__main__":
    vcf_to_custom_haplo(sys.argv[1], sys.argv[2], sys.argv[3])
=======
with open(hap_path, "w") as file:
    i = 1
    for key, value in sample_records.items():
        str1 = []
        str2 = []
        
        for v in value:
            str1.append(str(v[0] + 1))
            str2.append(str(v[1] + 1))
        
        str1 = ''.join(str1)
        str2 = ''.join(str2)
        
        samples[key] = [str1, str2]
        
        substr1 = str1[:window_size]
        substr2 = str2[:window_size]
        combined_substr = substr1 + substr2
        
        if substr1 not in string_ids:
            string_ids[substr1] = id1
            id1 += 1
        h1 = string_ids[substr1]
        if substr2 not in string_ids:
            string_ids[substr2] = id1
            id1 += 1
        h2 = string_ids[substr2]
        if combined_substr not in string_ids:
            string_ids[combined_substr] = id2
            id2 += 1
        d = string_ids[combined_substr]
        
        file.write(f'{i}\t{d}\t{h1}\t{h2}\t{substr1}\t{substr2}\n') # tab delimited for readability
        i += 1

#print(f'{list(samples.keys())[0]}: {list(samples.values())[0]}')

print(f'output wirten to {hap_path}')
>>>>>>> origin/master:vcfToHap.py
