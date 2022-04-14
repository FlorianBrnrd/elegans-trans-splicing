
# Caenorhabditis elegans trans-splicing


This repository contains the code used for generating the figures depicted in the following paper: **Quantitative analysis of *C. elegans* transcripts by Nanopore direct cDNA sequencing reveals terminal hairpins in non trans- spliced mRNAs.** Bernard, et al. 2022.


### Authors

- [Florian Bernard ¹𝄒²](https://www.github.com/FlorianBrnrd)
- Delphine Dargere ¹
- [Oded Rechavi ²](https://www.odedrechavilab.com/)
- [Denis Dupuy ¹](http://www.iecb.u-bordeaux.fr/teams/DUPUY/DupuylabSite/Welcome.html)


¹ Université de Bordeaux, Inserm U1212, CNRS UMR5320 , Institut Européen de Chimie et Biologie (IECB), 2, rue Robert Escarpit, 33607 Pessac, France.

² Department of Neurobiology, Wise Faculty of Life Sciences & Sagol School of Neuroscience, Tel Aviv University, Tel Aviv, Israel.

&nbsp;


## Data availability

The direct-cDNA datasets used in this study have been deposited in the Sequence Read Archive (SRA) under the following accession code: **PRJNA822363**.

The processed **dataset**, along with the necessary files for running the notebooks locally have been deposited on Figshare (DOI: 10.6084/m9.figshare.19131260).

&nbsp;


## Repository organization

A preprocessing notebook is available for generating the dataset table used in all downstream analysis from SAM/BAM alignments files (retrieved from our SRA archive or for analyzing your own alignment files).

A separate notebook was then generated for each of the figures shown in the paper as detailed above: 

| Notebook                                                                                                                       | Figure       | Title                                                             |
|--------------------------------------------------------------------------------------------------------------------------------|--------------|-------------------------------------------------------------------|
| [preprocessing](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/preprocessing.ipynb) | -            |Pipeline for processing alignments and generating the dataset table |
| [Fig1_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig1_notebook.ipynb) | Fig. 1a&d    |Measure of strand bias in direct-cDNA experiments                  |
| [Fig1_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig1_notebook.ipynb) | Fig. 1b      |Measure of base quality in 5' soft-clip region and alignment region |
| [Fig2_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig2_notebook.ipynb) | Fig. 2b      |Measure of total SL1 and SL2 variants detected in our reads        |
| [Fig3_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig3_notebook.ipynb) | Fig. 3a      |Splice leader usage                                                |
| [Fig3_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig3_notebook.ipynb) | Fig. 3b      |SL2 gene specificity                                               |
| [Fig4_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig4_notebook.ipynb) | Fig. 4a      |Gene expression and trans-splicing status                          |
| [Fig4_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig4_notebook.ipynb) | Fig. 4b      |Trans-splicing detection level                                     |
| [Fig4_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig4_notebook.ipynb) | Fig. 4c      |Poorly trans spliced mRNA have a propensity to form a 5’ stem loop structure |
| [Fig5_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig5_notebook.ipynb) | Fig. 5a      |Measure of base quality for SL, Hairpin and Unidentified reads     |
| [Fig5_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig5_notebook.ipynb) | Fig. 5b      |Repartition of SL, Hairpin and Unidentified reads in dataset       |
| [Fig5_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/Fig5_notebook.ipynb) | Fig. 5c      |Schematic representation of the trans-splicing information         |
| [SupFig_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/SupFig_notebook.ipynb) | Sup. Fig. 2  |Identification of direct-cDNA sequencing adapters                  |
| [SupFig_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/SupFig_notebook.ipynb) | Sup. Fig. 3  |Measured length of 5’ and 3’ soft-clips                            |
| [SupFig_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/SupFig_notebook.ipynb) | Sup. Fig. 4a |Origin of supplementary alignments                                           |
| [SupFig_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/SupFig_notebook.ipynb) | Sup. Fig. 4b |Size distribution of supplementary alignments                                |
| [SupFig_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/SupFig_notebook.ipynb) | Sup. Fig. 5  |Measure of base quality across all sequencing experiments                    |
| [SupFig_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/SupFig_notebook.ipynb) | Sup. Fig. 6  |Strand bias in ONT direct-cDNA experiments                                   |
| [SupFig_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/SupFig_notebook.ipynb) | Sup. Fig. 7  |Method for evaluating base quality                                           |
| [SupFig_notebook](https://github.com/FlorianBrnrd/caenorhabditis-elegans-trans-splicing/blob/main/notebooks/SupFig_notebook.ipynb) | Sup. Fig. 8  |high confidence SL matchs are located near the alignment start               |


&nbsp;

## Generating your own plots
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/florianbrnrd/elegans-trans-splicing/main/app/streamlit_app.py)

This web-app allows you to generate and save plots for your genes of interests without having to run the notebooks.  
The app was made using the streamlit library (see [streamlit_app.py]()) and is hosted via streamlit sharing.

&ensp;


## License

The source code is licensed under the MIT License.
