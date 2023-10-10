import pysam

# Input VCF and output hap file paths
vcf_path = "OUT_VCF_BEAGLE4_ALL_AutoSom21b_Chr28.TxT.vcf.gz"
hap_path = "output.hap"

# Open the VCF file for reading
vcf = pysam.VariantFile(vcf_path)

# Open the HAP file for writing
hap_file = open(hap_path, "w")

# Write header to the HAP file (modify as needed)
hap_file.write("HAPLOTYPE\n")

# Iterate through VCF records and write haplotypes
for record in vcf:
    # Extract relevant information from the VCF record
    chrom = record.contig
    pos = record.pos
    ref = record.ref
    alts = record.alts
    ht = "nada"
    #ht = record.info[""]

    # Write haplotype information to the HAP file (modify as needed)
    hap_file.write(f"{record}\t{ht}\t{chrom}\t{pos}\t{ref}\t{','.join(alts)}\n")

    break

hap_file.write(f"\nTotal samples: {len(list(vcf.header.samples))}")
hap_file.write(f"\n Header info: {list(vcf.header.info)}")

# Close the HAP file
hap_file.close()

# Close the VCF file
vcf.close()
