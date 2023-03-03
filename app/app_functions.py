import os
import re
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
import base64
import plotly.io as pio


def isoform_to_gene(isoform):
    match = re.search(r"\w+.\d+", isoform)
    return match[0] if match is not None else None


@st.cache_data(show_spinner=False)
def get_gene_ref(genes, GENES):
    GENESNAME = genes[genes['CDS'].isin(GENES)]
    GENESNAME['name'] = GENESNAME.apply(lambda x: x['name'] if x['name'] == x['name'] else x['CDS'], axis=1)
    GENESNAME = GENESNAME.iloc[GENESNAME.name.str.lower().argsort()]
    GENESNAME = GENESNAME.set_index('CDS')['name'].to_dict()

    return GENESNAME


@st.cache_data(show_spinner=False)
def get_atg_position(atg):
    # convert transcript name to gene name
    atg['gene'] = atg['transcript'].apply(lambda x: isoform_to_gene(x))
    return {gene: list(set(positions['CDS_start'])) for gene, positions in atg.groupby('gene')}


@st.cache_data(show_spinner=False)
def get_reference_files():
    path = os.getcwd()

    exons = pd.read_csv(f'{path}/app/src/exon_coordinates.tsv', sep='\t')
    genes = pd.read_csv(f'{path}/app/src/genes_coordinates.tsv', sep='\t')
    dataset = pd.read_csv(f'{path}/app/src/SL_&_mimic_positions.tsv', sep='\t')
    atg = pd.read_csv(f'{path}/app/src/CDS_start_positions.tsv', sep='\t')

    GENES = list(set(dataset['gene']))
    GENESNAME = get_gene_ref(genes, GENES)
    ATGPOSITIONS = get_atg_position(atg)

    return genes, exons, dataset, GENES, GENESNAME, ATGPOSITIONS


def get_legend_filepath(legend_type):
    path = os.getcwd()
    return f'{path}/app/src/legend.png' if legend_type == 'plot1' else f'{path}/app/src/features_legend.png'


def overlapping_exons(start, end, exon):
    x, y = exon
    return not x <= start < y and not x <= end < y


def plotly_gene_structure(fig, gene, genes_coord, exons_coord):

    # Select exons for gene of interest and remove duplicates
    exons_coord = exons_coord.loc[exons_coord['gene'] == gene].drop_duplicates(['start', 'end']).sort_values('start')

    #### DRAW LINE FIRST

    # get start / end coordinates for the gene
    gene_start = genes_coord.loc[genes_coord['CDS'] == gene, 'start'].values[0]
    gene_end = genes_coord.loc[genes_coord['CDS'] == gene, 'end'].values[0]

    # Calculate isoform length
    gene_length = gene_end - gene_start

    # Create gene line to be plotted
    fig.add_shape(type="line", x0=gene_start, y0=0.5, x1=gene_end, y1=0.5,
                  line=dict(color="black", width=1.5),
                  row=1, col=1)

    #### THEN DRAW EXONS

    # Process exons
    exons_set = []

    for _, exon in exons_coord.iterrows():

        start = exon['start']
        end = exon['end']

        set_size = len(exons_set)

        if set_size == 0:
            exons_set.append((start, end))

        elif all(overlapping_exons(start, end, exons_set[n]) for n in range(set_size)):
            exons_set.append((start, end))

    strand = exons_coord['strand'].unique()[0]

    l = gene_length + gene_length * 0.2
    arrow_size = 0.02 * l

    for i, exon in enumerate(exons_set):

        start, end = exon
        length = abs(start - end)

        # bleu fleche vers la gauche (antisense strand last exon)
        if strand == '-' and i == 0:

            if arrow_size <= length:

                xn = start + arrow_size

                fig.add_shape(type="path", path=f' M{start},0.5 L{xn},1 H{end} V0, H{xn} Z',
                              fillcolor="LightSkyBlue",
                              line=dict(color="black", width=2),
                              row=1, col=1)

            else:

                fig.add_shape(type="path", path=f' M{start},0.5 L{end},1 V0 Z',
                              fillcolor="LightSkyBlue",
                              line=dict(color="black", width=2),
                              row=1, col=1)

        elif strand == '-' and i > 0:

            fig.add_shape(type="rect", x0=start, y0=0, x1=end, y1=1,
                          line=dict(color="black", width=2), fillcolor="LightSkyBlue",
                          row=1, col=1)

        # sense strand last exon
        elif strand == '+' and i + 1 == len(exons_set):

            if arrow_size <= length:

                xn = end - arrow_size

                fig.add_shape(type="path", path=f' M{start},0 V1 H{xn} L{end},0.5 L{xn},0 Z',
                              fillcolor="LightPink",
                              line=dict(color="black", width=2),
                              row=1, col=1)
            else:

                fig.add_shape(type="path", path=f' M{start},0  V1 L{end},0.5 Z',
                              fillcolor="LightSkyBlue",
                              line=dict(color="black", width=2),
                              row=1, col=1)

        # sense strand
        elif strand == '+' and i < len(exons_set):

            fig.add_shape(type="rect", x0=start, y0=0, x1=end, y1=1,
                          line=dict(color="black", width=2), fillcolor="LightPink",
                          row=1, col=1)

        # unknown strand
        else:

            fig.add_shape(type="rect", x0=start, y0=0, x1=end, y1=1,
                          line=dict(color="black", width=2), fillcolor="grey",
                          row=1, col=1)

    return gene_start, gene_end, gene_length


def plot_gene_start(dataset, gene, genes_coord, exons_coord, ATGPOSITION, show_atg=True):

    fig = make_subplots(rows=2, cols=1, row_heights=[2, 10], shared_xaxes=True, vertical_spacing=0.02)

    # plot gene model ---------------------------------
    start, end, length = plotly_gene_structure(fig, gene, genes_coord, exons_coord)

    # lock y axis range on gene model subplot and remove axis/grid/etc
    fig.update_yaxes(fixedrange=True, range=[-1, 2], row=1, col=1)
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_yaxes(visible=False, row=1, col=1)

    # plot gene data points ---------------------------------

    gene_data = dataset[dataset['gene'] == gene]

    x = list(gene_data['position'])
    y = list(gene_data['total'])

    r = [i / 100 * 255 for i in list(gene_data['%SL'])]
    g = [i / 100 * 255 for i in list(gene_data['%hairpin'])]
    b = [i / 100 * 255 for i in list(gene_data['%unidentified'])]
    col = list(zip(r, g, b))
    col = [f'rgb({r},{g},{b})' for r, g, b in list(col)]

    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(color=col, size=10)), row=2, col=1)

    # plot ATG ---------------------------------

    if show_atg and gene in ATGPOSITION:
        ATG = ATGPOSITION[gene]

        for _atg in ATG:
            fig.add_vline(x=_atg, line_width=2, line_dash="dot", line_color="#36454F", row=2, col=1, layer='below')

    # add custom hovering infos ---------------------------------

    gene_data['SL2_ratio'] = round(gene_data['SL2_ratio'] * 100, 2)
    gene_data['SL2_ratio'] = gene_data['SL2_ratio'].fillna('N/A')

    cstm = np.stack((gene_data['%SL'], gene_data['%hairpin'], gene_data['%unidentified'], gene_data['SL2_ratio']),
                    axis=-1)

    hovertemplate = ('<b>Position:</b> %{x}<br>'
                     '<b>Reads:</b> %{y}<br>' +
                     '<br>' +
                     '<b>SL:</b> %{customdata[0]}% | <b>SL2 ratio:</b> %{customdata[3]}%<br>' +
                     '<b>Hairpin:</b> %{customdata[1]}%<br>' +
                     '<b>Unknown:</b> %{customdata[2]}%<br>' +
                     '<extra></extra>')

    fig.update_traces(customdata=cstm, hovertemplate=hovertemplate, row=2, col=1)

    # add x and y axis labels ---------------------------------

    fig['layout']['yaxis2']['title'] = '<b>Number of reads</b>'
    fig['layout']['xaxis2']['title'] = '<b>genomic start position (bp)</b>'

    # plots settings ---------------------------------

    _start = start - (length * 0.1)
    _end = end + (length * 0.1)
    max_val = max(y)

    fig.update_layout(xaxis_range=[_start, _end], yaxis2 = dict(range=[-(0.05*max_val), (max_val*1.05)]),
                      width=890, height=500, margin=dict(l=0, r=10, b=0, t=0),
                      plot_bgcolor="rgb(255,255,255,255)")

    fig.update_yaxes(zeroline=False, showline=True, linewidth=1.2, linecolor='#36454F', mirror=True,
                     showgrid=True, gridwidth=0.5, gridcolor='lightgrey',
                     tickformat=',', ticks="outside", tickcolor='black', ticklen=5,
                     tickfont=dict(size=12, color='#36454F', family='Roboto'),
                     title_font=dict(size=16, color='#36454F', family='Roboto'))

    fig.update_xaxes(zeroline=False, showline=True, linewidth=1.2, linecolor='#36454F', mirror=True,
                     showgrid=True, gridwidth=0.5, gridcolor='lightgrey',
                     tickformat=',', ticksuffix='bp', tickfont=dict(size=12, color='#36454F', family='Roboto'),
                     ticks="outside", tickcolor='black', ticklen=5,
                     title_font=dict(size=16, color='#36454F', family='Roboto'))

    return fig


def download_plotly_static(fig, gene, generef):
    st.sidebar.markdown('### 3. Save plot:')

    if generef is not None:
        name_template = f'<b>{gene} ({generef}) </b>'
    else:
        name_template = f'<b>{gene}</b>'

    # modify layout for pdf + add title
    _fig = fig.update_layout(margin=dict(l=100, r=100, b=100, t=100), title_text=name_template, title_font_size=30,
                             title_font_family='Roboto', title_font_color='black')

    # set explicit headless parameters for chromium (not sure if all are needed)
    pio.kaleido.scope.chromium_args = (
        "--headless",
        "--no-sandbox",
        "--single-process",
        "--disable-gpu")  # tuple with chromium args

    # create pdf file and store in memory as bytes for st.download_button
    plot_bytes = _fig.to_image(format="png", width=1200, height=900, scale=2)
    st.sidebar.download_button('📥 Download', plot_bytes, file_name='test.png')


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    return base64.b64encode(img_bytes).decode()
