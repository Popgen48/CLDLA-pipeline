# Simple script to extract the values from all the samples of a given .VCF file, assign them an id and store in a .hap file
import sys
import os
import util
import pysam

g_list_geno_dict = [{}]
g_list_maf_dict = [{}]
g_list_homo_dict = [{}]
g_list_pos_dict = [{}]


def read_vcf(vcf_path, window_size):
    window_size = int(window_size)
    vcf = pysam.VariantFile(vcf_path)
    dataset = vcf_path.split(".")[0]
    chromosome = vcf_path.split(".")[1]
    window_number = 0

    # Iterate through VCF records
    for i, record in enumerate(vcf):
        last_ele = -1
        is_window_size = (
            False if len(list(g_list_maf_dict[last_ele].keys())) < window_size else True
        )
        maf = util.get_maf(record)
        # calculate maf only collect the genotypes if the maf is grt than 0
        if maf[0] != 0 and maf[1] != 0:
            if not record.id:
                record.id = f"{record.chrom}_{record.pos}"
            homozygosity = util.get_homozygosity(maf)
            while not is_window_size and not len(g_list_maf_dict) + last_ele == 0:
                # While maf is collected here, it is not used in downstream analysis
                g_list_maf_dict[last_ele][record.id] = min(maf) / sum(maf)
                g_list_homo_dict[last_ele][record.id] = homozygosity
                g_list_pos_dict[last_ele][record.id] = record.pos / 1e6

                # Iterate through samples
                for sample in record.samples:
                    sample_values = record.samples[sample]["GT"]
                    if sample not in g_list_geno_dict[last_ele]:
                        g_list_geno_dict[last_ele][sample] = []
                    g_list_geno_dict[last_ele][sample].append(sample_values)

                last_ele += -1

                if len(g_list_maf_dict) > 1:
                    is_window_size = (
                        False
                        if len(list(g_list_maf_dict[last_ele].keys())) < window_size
                        else True
                    )
                else:
                    is_window_size = True
            g_list_maf_dict.append({record.id: min(maf) / sum(maf)})
            g_list_homo_dict.append({record.id: homozygosity})
            g_list_pos_dict.append({record.id: record.pos / 1e6})
            g_list_geno_dict.append({})
            for sample in record.samples:
                sample_values = record.samples[sample]["GT"]
                g_list_geno_dict[-1][sample] = [sample_values]
            if len(g_list_maf_dict[1]) == window_size:
                sample_genotypes = g_list_geno_dict[1]
                positions = g_list_pos_dict[1]
                hzgys = g_list_homo_dict[1]
                window_number += 1
                write_output_files(
                    dataset,
                    chromosome,
                    sample_genotypes,
                    positions,
                    hzgys,
                    window_number,
                    window_size,
                )
                del g_list_geno_dict[1]
                del g_list_pos_dict[1]
                del g_list_maf_dict[1]
                del g_list_homo_dict[1]
                print(f"wrote window number {window_number}")

    print(g_list_geno_dict)
    print(g_list_maf_dict)
    vcf.close()


def write_output_files(
    dataset, chromosome, sample_genotypes, positions, hzgys, window_number, window_size
):

    if not os.path.exists(f"./{dataset}/{chromosome}"):
        os.makedirs(f"./{dataset}/{chromosome}")

    hap_path = f"./{dataset}/{chromosome}/{dataset}.{chromosome}.{window_number+1}.hap"
    map_path = f"./{dataset}/{chromosome}/{dataset}.{chromosome}.{window_number+1}.map"
    par_path = f"./{dataset}/{chromosome}/{dataset}.{chromosome}.{window_number+1}.par"

    n_samples = util.get_HAP(hap_path, sample_genotypes)
    util.get_MAP(map_path, positions, hzgys)
    util.get_PAR(par_path, window_size, window_number, n_samples)

    print(f"Generated .hap, .map, and .par for window {window_number+1}")


if __name__ == "__main__":
    read_vcf(sys.argv[1], sys.argv[2])
