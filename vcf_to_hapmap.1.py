# Simple script to extract the values from all the samples of a given .VCF file, assign them an id and store in a .hap file
import sys
import os
import util
import pysam
import subprocess

g_list_geno_dict = [{}]
g_list_maf_dict = [{}]
g_list_homo_dict = [{}]
g_list_pos_dict = [{}]

# set the working directory to the script's location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)


def get_homozygosity(list):
    return (list[0] ** 2 + list[1] ** 2) / (sum(list) ** 2)


def make_sample_list(incl_samples):
    sample_list = []
    with open(incl_samples) as source:
        for line in source:
            line = line.rstrip().split()
            sample_list.append(line[0])
    return sample_list


def get_maf(record, sample_list):
    ac = [0, 0]
    for val in sample_list:
        if record.samples[val]["GT"][0] != None:
            ac[record.samples[val]["GT"][0]] += 1
        if record.samples[val]["GT"][1] != None:
            ac[record.samples[val]["GT"][1]] += 1
    return ac


def read_vcf(
    vcf_path,
    window_size,
    incl_samples,
    maf_threshold,
):
    sample_list = make_sample_list(incl_samples)
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
        ac = get_maf(record, sample_list)
        maf = min(ac) / sum(ac)
        # calculate maf only collect the genotypes if the maf is grt than the threshold
        if maf > float(maf_threshold):
            if not record.id:
                record.id = f"{record.chrom}_{record.pos}"
            homozygosity = get_homozygosity(ac)
            while not is_window_size and not len(g_list_maf_dict) + last_ele == 0:
                # While maf is collected here, it is not used in downstream analysis
                g_list_maf_dict[last_ele][record.id] = maf
                g_list_homo_dict[last_ele][record.id] = homozygosity
                g_list_pos_dict[last_ele][record.id] = record.pos / 1e6

                # Iterate through samples
                for sample in sample_list:
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
            g_list_maf_dict.append({record.id: maf})
            g_list_homo_dict.append({record.id: homozygosity})
            g_list_pos_dict.append({record.id: record.pos / 1e6})
            g_list_geno_dict.append({})
            for sample in sample_list:
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
    vcf.close()


def write_output_files(
    dataset, chromosome, sample_genotypes, positions, hzgys, window_number, window_size
):

    # if not os.path.exists(f"./{dataset}/{chromosome}"):
    #    os.makedirs(f"./{dataset}/{chromosome}")
    prefix = f"{dataset}.{chromosome}.{window_number}"
    hap_path = f"{prefix}.Hap"
    map_path = f"{prefix}.Map"
    par_path = f"{prefix}.par"

    n_samples, max_d = util.get_HAP(hap_path, sample_genotypes)
    util.get_MAP(map_path, positions, hzgys)
    util.get_PAR(par_path, window_size, window_number, n_samples)

    with open(f'{window_number}.info','w') as dest:
        dest.write(f'{prefix} {max_d}\n')

    #command = f"{dname}/cLDLA_snp {prefix} && {dname}/Bend5 {prefix}.grm {prefix}.B.grm && {dname}/ginverse_o3 {max_d} {prefix}.B.grm {prefix}.giv"
    #subprocess.call([command], shell=True)

    print(f"Generated .hap, .map, and .par for window {window_number}")


if __name__ == "__main__":
    read_vcf(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
