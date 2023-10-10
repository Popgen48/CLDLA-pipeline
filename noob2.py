# Simple script to extract the values from all the samples of a given .VCF file

# TODO: get SNPs for a given sample, count the frequency of the maternal and paternal haplotype strings...

import pysam

# Input VCF and output hap file paths
vcf_path = "OUT_VCF_BEAGLE4_ALL_AutoSom21b_Chr28.TxT.vcf.gz"
hap_path = "output.hap"

vcf = pysam.VariantFile(vcf_path)

hap_file = open(hap_path, "w")

# dictionary to store samples
sample_records = {}

# Iterate through VCF records
for record in vcf:
    # Iterate through samples
    for sample in record.samples:
        sample_name = sample
        sample_values = record.samples[sample]['GT']
        #print(sample_values)

        if sample_name not in sample_records:
            sample_records[sample_name] = []

        sample_records[sample_name].append(sample_values)


vcf.close()

#print(sample_records.keys())
print(f'{list(sample_records.keys())[0]}: {list(sample_records.values())[0]}')
