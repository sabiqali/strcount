# STRcount
Software tool to analyse STR loci from long read data. STRcount can count the number of repeats in a repeat expansion and give you the count in a tabular format for further downstream analysis.

## Release notes
* 0.1.0: Initial release with tools updated on Pypi and ready to use.

## Dependencies
Developed and tested on Python 3.7.10. Dependencies include:
* [GraphAligner](https://github.com/maickrau/GraphAligner)
* [Pysam](https://github.com/pysam-developers/pysam)

## Installation instructions

### Install GraphAligner

STRcount requires and uses GraphAligner as it's alignment tool. To install this you could either install it using Anaconda:
* Install miniconda https://conda.io/projects/conda/en/latest/user-guide/install/index.html
* ```conda install -c bioconda graphaligner```

Or you could install it from source using the instructions [here](https://github.com/maickrau/GraphAligner#compilation)

### Installation using pip

Use the following command to install STRcount and all dependencies:
```
pip install STRcount
```

### Installation from source

```
git clone https://github.com/sabiqali/strcount.git
cd strcount
python setup.py install
```

### Installation to develop

To develop using STRcount, you will need to create a conda environment or python virtual environment, then perform the following steps:
```
git clone https://github.com/sabiqali/strcount.git
cd strcount
python -m pip install -r requirements.txt
python src/STRcount/STRcount.py -h
```

## Config file format

 The config file should be in the following format:
 
 | chr | begin | end | name | repeat | prefix | suffix | 
 | --- | --- | --- | --- | --- | --- | --- | 
 | chr9 | 27573527 | 27573544 | c9orf72 | GGCCCC | <150bp_left_flank> | <150bp_right_flank> | 
 
 ## Usage
 
 If installed using pip or from source, you will be able to use it using ```STRcount``` else if you have installed to develop, you will be able to use it using ```python src/STRcount/STRcount.py```
 
 ```
 STRcount [-h] --reference REFERENCE --fastq FASTQ --config CONFIG
                   --output OUTPUT [--min-identity MIN_IDENTITY]
                   [--min-aligned-fraction MIN_ALIGNED_FRACTION]
                   [--write-non-spanned]
                   [--repeat_orientation REPEAT_ORIENTATION]
                   [--prefix_orientation PREFIX_ORIENTATION]
                   [--suffix_orientation SUFFIX_ORIENTATION]
                   [--cleanup CLEANUP] [--output_directory OUTPUT_DIRECTORY]
                   [--multiseed-DP MULTISEED_DP]
                   [--precise-clipping PRECISE_CLIPPING]

optional arguments:
  -h, --help            show this help message and exit
  --reference REFERENCE
                        the reference from which the STR Graph will be
                        generated
  --fastq FASTQ         the baseaclled reads in fastq format
  --config CONFIG       the config file
  --output OUTPUT       the output file
  --min-identity MIN_IDENTITY
                        only use reads with identity greater than this
  --min-aligned-fraction MIN_ALIGNED_FRACTION
                        require alignments cover this proportion of the query
                        sequence
  --write-non-spanned   do not require the reads to span the prefix/suffix
                        region
  --repeat_orientation REPEAT_ORIENTATION
                        the orientation of the repeat string. + or -
  --prefix_orientation PREFIX_ORIENTATION
                        the orientation of the prefix, + or -
  --suffix_orientation SUFFIX_ORIENTATION
                        the orientation of the suffix, + or -
  --cleanup CLEANUP     do you want to clean up the temporary file?
  --output_directory OUTPUT_DIRECTORY
                        the output directory for all output and temporary
                        files
  --multiseed-DP MULTISEED_DP
                        Aligner option
  --precise-clipping PRECISE_CLIPPING
                        Aligner option: use arg as the identity threshold for
                        a valid alignment.
```
                        
                        
 ## Output

The output is in a ```.tsv``` format that will look something like this:
| read_name | strand | spanned | count | align_score | identity | query_aligned_fraction | 
| --- | --- | --- | --- | --- | --- | --- | 

* read_name: The name of the read that is currently being proccessed
* strand: The strand on which the primary alignment has been detected
* spanned: If set to 1, it means that the read spanned the repeat locus and the flanking sequence
* count: The number of repeat motifs detected at the locus for that particular read
* align_score: The alignment score as given by GraphAligner
* identity: The percentage identity as given by GraphAligner
* query_aligned_fraction: This signifies how much of the query sequence is covered by the alignment

 ## Contact

[Sabiq Chaudhary](mailto:schaudhary@oicr.on.ca)

## License

```MIT```
