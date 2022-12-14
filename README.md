
# Caenorhabditis elegans trans-splicing


This repository contains the code used for generating the figures depicted in the following paper: **Quantitative analysis of *C. elegans* transcripts by Nanopore direct cDNA sequencing reveals terminal hairpins in non trans- spliced mRNAs.** Bernard, et al. 2022.

The manuscript is available on [BioRxiv](https://www.biorxiv.org/content/10.1101/2022.04.14.488332v1).

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

The processed **[dataset](https://doi.org/10.6084/m9.figshare.19131260.v1)**, along with the necessary files for running the notebooks locally have been deposited on Figshare (DOI: 10.6084/m9.figshare.19131260).

&nbsp;


## Repository organization

A preprocessing notebook is available for generating the dataset table used in all downstream analysis from SAM/BAM alignments files (retrieved from our SRA archive or for analyzing your own alignment files).

A separate notebook was then generated for each of the figures shown in the paper as detailed above: 

| Notebook                                                                                                                | Figure       | Title                                                                        |
|-------------------------------------------------------------------------------------------------------------------------|--------------|------------------------------------------------------------------------------|
| [pre-processing](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/pre-processing.ipynb)       | -            | Pipeline for processing alignments and generating the dataset table          |
| [Fig1_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig1_notebook.ipynb)         | Fig. 1b      | Measure of base quality in 5' soft-clip region and alignment region          |
| [Fig2_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig2_notebook.ipynb)         | Fig. 2b      | Measure of total SL1 and SL2 variants detected in our reads                  |
| [Fig3_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig3_notebook.ipynb)         | Fig. 3a      | Spliced leader usage                                                         |
| [Fig3_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig3_notebook.ipynb)         | Fig. 3b      | SL2 gene specificity                                                         |
| [Fig4_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig4_notebook.ipynb)         | Fig. 4a      | Gene expression and trans-splicing status                                    |
| [Fig4_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig4_notebook.ipynb)         | Fig. 4b      | Trans-splicing detection level                                               |
| [Fig4_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig4_notebook.ipynb)         | Fig. 4c      | Poorly trans spliced mRNA have a propensity to form a 5’ stem loop structure |
| [Fig5_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig5_notebook.ipynb)         | Fig. 5a      | Measure of ratio SL/Hairpin                                                  |
| [Fig5_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig5_notebook.ipynb)         | Fig. 5b      | Proportion of trans-spliced gene with various SL thresholds                  |
| [Fig5_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig5_notebook.ipynb)         | Fig. 5c      | Read coverage for SL, Hairpin and Unidentified genes                         |
| [Fig6_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/Fig6_notebook.ipynb)         | Fig. 6       | Schematic representation of the trans-splicing information                   |
| [SupFig1_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig1_notebook.ipynb)   | Sup. Fig. 1  | Measure of strand bias in direct-cDNA experiments                            |
| [SupFig2_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig2_notebook.ipynb)   | Sup. Fig. 2b | Measured length of 5’ and 3’ soft-clips                                      |
| [SupFig3_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig3_notebook.ipynb)   | Sup. Fig. 3a | Quantification of sequencing adapters in soft-clips regions                  |
| [SupFig3_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig3_notebook.ipynb)   | Sup. Fig. 3b | Origin of supplementary alignments                                           |
| [SupFig3_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig3_notebook.ipynb)   | Sup. Fig. 3c | Size distribution of supplementary alignments                                |
| [SupFig4_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig4_notebook.ipynb)   | Sup. Fig. 4  | Measure of base quality across all sequencing experiments                    |
| [SupFig5_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig5_notebook.ipynb)   | Sup. Fig. 5a | Measure of read length and alignment length across experiments               |
| [SupFig5_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig5_notebook.ipynb)   | Sup. Fig. 5b | Measure of read coverage                                                     |
| [SupFig6_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig6_notebook.ipynb)   | Sup. Fig. 6a | Strand orientation for unidentified reads                                    |
| [SupFig6_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig6_notebook.ipynb)   | Sup. Fig. 6b | Length of 5’ soft-clips versus their alignment length                        |
| [SupFig7_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig7_notebook.ipynb)   | Sup. Fig. 7a | Single SL1 promotor - nlp-36 (B0464.3)                                       |
| [SupFig7_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig7_notebook.ipynb)   | Sup. Fig. 7b | Multiple SL1 promotors - M60.4                                               |
| [SupFig7_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig7_notebook.ipynb)   | Sup. Fig. 7c | Operon organization - rla-1 (Y37E3.8) & Y37E3.7                              |
| [SupFig7_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig7_notebook.ipynb)   | Sup. Fig. 7d | Differentially trans-spliced promoters - lev-11 (Y105E8B.1)                  |
| [SupFig8_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig8_notebook.ipynb)   | Sup. Fig. 8a | Measure of strand bias at each locus in SSP experiments                      |
| [SupFig8_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig8_notebook.ipynb)   | Sup. Fig. 8b | Unbiased locus presents a high concentration of SSP reads                    |
| [SupFig8_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig8_notebook.ipynb)   | Sup. Fig. 8c | Unbiased locus in SSP Exp. are found biased in SL1/NP Exp                    |
| [SupFig9_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig9_notebook.ipynb)   | Sup. Fig. 9 | Method for evaluating base quality                                           |
| [SupFig10_notebook](https://github.com/FlorianBrnrd/elegans-trans-splicing/blob/main/notebooks/SupFig10_notebook.ipynb) | Sup. Fig. 10 | high confidence SL matchs are located near the alignment start               |

&nbsp;

## Generating your own plots
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://elegans-trans-splicing.streamlit.app/)

This web-app allows you to generate and save plots for your genes of interests without having to run the notebooks.  
The app was made using the streamlit library (see [streamlit_app.py](https://elegans-trans-splicing.streamlit.app/)) and is hosted via streamlit sharing.

&ensp;


## License

The source code is licensed under the MIT License.
