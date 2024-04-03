import sys
import os
import pysam
import subprocess
import argparse
from multiprocessing import Pool
from filter_vcf import make_sample_list

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

g_list_geno_dict = [{}]
g_list_homo_dict = [{}]
g_list_pos_dict = [{}]
g_job_list = []


def prepare_dat_file(hap_path, pheno_file, prefix):
    indi_diplo_dict = {}
    with open(prefix + ".dat", "w") as dest:
        with open(hap_path) as source:
            lc = 0
            for line in source:
                diplo = line.rstrip().split()[3]
                indi_diplo_dict[lc] = diplo
                lc += 1
        with open(pheno_file) as source:
            lc = 0
            for line in source:
                line = line.rstrip().split()
                line.append(indi_diplo_dict[lc])
                dest.write(" ".join(line))
                lc += 1


def prepare_asreml_params(infile, numdiplo, grm, prefix):
    outfile = f"{prefix}.as"
    ilc = 0
    with open(outfile, "w") as dest:
        with open(infile) as source:
            for line in source:
                line = line.rstrip()
                if not line.startswith("!") and ilc == 0:
                    dest.write(line)
                    dest.write("\n")
                elif ilc == 0:
                    dest.write(f"iDip {numdiplo} {line}")
                    dest.write("\n")
                    ilc += 1
                elif ilc == 1:
                    dest.write(f"{grm} {line}")
                    dest.write("\n")
                    ilc += 1
                elif ilc == 2:
                    dest.write(f"{prefix}.giv {line}")
                    dest.write("\n")
                    ilc += 1
                elif ilc == 3:
                    dest.write(f"{prefix}.dat {line}")
                    dest.write("\n")
                    ilc += 1
                elif ilc == 4:
                    dest.write(f"{line}")
                    dest.write("\n")


def get_HAP(hap_path, sample_genotypes):
    samples = {}
    string_ids = {}  # dictionary to store counts
    id1 = 1  # for individual haplotypes
    id2 = 1  # for combined haplotypes i.e. diplotype
    max_d = 0

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
            max_d = d if d > max_d else max_d
            str1 = " ".join(list(str1))
            str2 = " ".join(list(str2))
            file.write(f"{i} {h1} {h2} {d} {str1} {str2}\n")  # tab delimited for readability
            i += 1
    return len(samples), max_d


def get_MAP(map_path, positions, hzgys):
    with open(map_path, "w") as file:
        for key in hzgys.keys():
            file.write(f"{key} {positions[key]} {hzgys[key]}\n")


def get_PAR(par_path, window_size, window_number, n_samples):
    with open(par_path, "w") as file:
        file.write(
            f"100\n100\n{window_size+1}\n{window_number if window_number <= int(window_size/2) else int(window_size/2)+1}\n{n_samples}"
        )


def get_homozygosity(list):
    return (list[0] ** 2 + list[1] ** 2) / (sum(list) ** 2)


def get_maf(record, sample_list):
    ac = [0, 0]
    for val in sample_list:
        if record.samples[val]["GT"][0] != None:
            ac[record.samples[val]["GT"][0]] += 1
        if record.samples[val]["GT"][1] != None:
            ac[record.samples[val]["GT"][1]] += 1
    return ac


def read_vcf(vcf_path, chromosome, window_size, num_cores, grm, pheno_file, param_file, tool, outprefix):
    window_size = int(window_size)
    vcf = pysam.VariantFile(vcf_path)
    sample_list = make_sample_list(pheno_file)
    dataset = outprefix
    window_number = 0
    window_process_list = []

    # Iterate through VCF records
    for i, record in enumerate(vcf):
        last_ele = -1
        is_window_size = False if len(list(g_list_homo_dict[last_ele].keys())) < window_size else True
        ac = get_maf(record, sample_list)
        if not record.id:
            record.id = f"{record.chrom}_{record.pos}"
        homozygosity = get_homozygosity(ac)
        while not is_window_size and not len(g_list_homo_dict) + last_ele == 0:
            g_list_homo_dict[last_ele][record.id] = homozygosity
            g_list_pos_dict[last_ele][record.id] = record.pos / 1e6

            # Iterate through samples
            for sample in sample_list:
                sample_values = record.samples[sample]["GT"]
                if sample not in g_list_geno_dict[last_ele]:
                    g_list_geno_dict[last_ele][sample] = []
                g_list_geno_dict[last_ele][sample].append(sample_values)

            last_ele += -1

            if len(g_list_homo_dict) > 1:
                is_window_size = False if len(list(g_list_homo_dict[last_ele].keys())) < window_size else True
            else:
                is_window_size = True
        g_list_homo_dict.append({record.id: homozygosity})
        g_list_pos_dict.append({record.id: record.pos / 1e6})
        g_list_geno_dict.append({})
        for sample in sample_list:
            sample_values = record.samples[sample]["GT"]
            g_list_geno_dict[-1][sample] = [sample_values]
        if len(g_list_homo_dict[1]) == window_size:
            sample_genotypes = g_list_geno_dict[1]
            positions = g_list_pos_dict[1]
            hzgys = g_list_homo_dict[1]
            window_number += 1
            window_process_list.append(f"{dataset}.{chromosome}.{window_number}.as")
            g_job_list.append(
                (
                    dataset,
                    chromosome,
                    sample_genotypes,
                    positions,
                    hzgys,
                    window_number,
                    window_size,
                    pheno_file,
                    param_file,
                    tool,
                    grm,
                )
            )
            del g_list_geno_dict[1]
            del g_list_pos_dict[1]
            del g_list_homo_dict[1]
            if len(g_job_list) == int(num_cores):
                with Pool(processes=len(g_job_list)) as pool:
                    pool.map(write_output_files, g_job_list, 1)
                del g_job_list[:]
    for i1, v1 in enumerate(window_process_list):
        run_asreml(v1)
    del window_process_list[:]
    vcf.close()


def write_output_files(input_list):

    (
        dataset,
        chromosome,
        sample_genotypes,
        positions,
        hzgys,
        window_number,
        window_size,
        pheno_file,
        params_file,
        tool,
        grm,
    ) = input_list
    prefix = f"{dataset}.{chromosome}.{window_number}"
    hap_path = f"{prefix}.Hap"
    map_path = f"{prefix}.Map"
    par_path = f"{prefix}.par"

    n_samples, max_d = get_HAP(hap_path, sample_genotypes)
    get_MAP(map_path, positions, hzgys)
    get_PAR(par_path, window_size, window_number, n_samples)

    prepare_dat_file(hap_path, pheno_file, prefix)

    if tool == "asreml":
        prepare_asreml_params(params_file, max_d, grm, prefix)

    command = (
        f"{dname}/cLDLA_snp {prefix} && {dname}/Bend5 {prefix}.grm {prefix}.B.grm && {dname}/ginverse {max_d} {prefix}.B.grm {prefix}.giv"
        + "&& rm "
        + prefix
        + ".{Hap,Map,par,grm,B.grim}"
    )

    subprocess.call([command], shell=True)

    print(f"Generated .dat and .giv for {window_number}")


def run_asreml(prefix):
    command = f"asreml -NS5 {prefix}"
    subprocess.call([command], shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="python script to create hap, map, par and giv file of windows count in cLDLA"
    )

    parser.add_argument("-v", "--vcf", metavar="String", help="input phased vcf", required=True)
    parser.add_argument("-r", "--chr", metavar="String", help="chromosome id as mentioned in vcf", required=True)
    parser.add_argument("-w", "--window_size", metavar="Int", help="window size", default=40, required=False)
    parser.add_argument(
        "-c", "--num_cpus", metavar="Int", help="number of windows to be run in parallel", default=8, required=False
    )
    parser.add_argument(
        "-g",
        "--grm",
        metavar="String",
        help="relationship matrix based on entire chromosome",
        required=True,
    )
    parser.add_argument("-p", "--pheno", metavar="String", help="phenotype file", required=True)
    parser.add_argument("-a", "--params", metavar="String", help="parameter file", required=True)
    parser.add_argument(
        "-t", "--tool", metavar="String", help="tool to be used --> asreml or blupf90", default="asreml", required=False
    )
    parser.add_argument("-o", "--outprefix", help="output prefix", required=True)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        read_vcf(
            args.vcf,
            args.chr,
            args.window_size,
            args.num_cpus,
            args.grm,
            args.pheno,
            args.params,
            args.tool,
            args.outprefix,
        )
