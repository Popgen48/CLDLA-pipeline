## Custom Scripts for the cLDLA (combined linkage disequilibrium and linkage analysis) pipeline

1. `vcf_to_hapmap.py`: Generate .hap, .map, and .par files for a particular window from a given .vcf file. Can also be used in parallel to generate .hap, .map, and .par files for all windows in a given .vcf file.

Usage: `python3 vcf_to_hapmap.py <vcf_file> <window_size> <window_number>`

Stores the output under `<dataset>/<chromosome>/` as `<dataset>.<chromosome>.<window_number>.hap/.map/.par`

---

2. `get_vcf_record_count.py`: Get the number of _valid_ records in a .vcf file. (based on minor allele frequency). Output is saved under `<chromosome>_window_counts.txt`

Usage: `python3 get_vcf_record_count.py <vcf_file> <chromosome> <window_size>`

---

3. `Bend5` and `bend.R`: Scripts used for bending the relation matrix (.grm) for making it invertible at a later stage. `Bend5` is an old fortran exceutable and `bend.R` is an R script based on the '[mbend](https://cran.r-project.org/web/packages/mbend/index.html)' R package.

Produces a '.B.grm' output file

Usage (bend5): `./Bend5 <input_file> <output_file>`

Usage (bend.R): `Rscript bend.R <input_file> <output_file> <bending_method>`

The R-script also provides an option of bending using 2 methods (Jorjani's and Schaeffer's, more at https://cran.r-project.org/web/packages/mbend/mbend.pdf)

---

4. `ginverse` and `ginverse.py`: Scripts to get the generalized-inverse of a matrix. `ginverse` is an old fortran executable and `ginverse.py` is a python script, both of which give the same ouput but the python script is less likely to run into dependency issues as the fortran executable needs an older version of gcc setup to work (see the `install-libgfortran.sh` for the setup). Also it is necessary to provide the number of rows in the fortran executable, which is dynamically adjusted in the python script.

Produces a '.giv' output file.

Usage (ginverse): `./ginverse <number_of_rows> <input_file> <output_file>`

Usage (ginverse.py): `python3 ginverse.py <input_file> <output_file>`
