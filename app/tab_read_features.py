from app_functions import get_legend_filepath, img_to_bytes
import pandas as pd
import os
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go


@st.cache_data(show_spinner=False)
def get_read_features_files():

    path = os.getcwd()

    transcripts = pd.read_csv(f'{path}/app/src/transcripts_length.tsv',
                              index_col='transcript', sep='\t')
    TRANSCRIPTS = transcripts["size"].to_dict()

    exons = pd.read_csv(f'{path}/app/src/exon_coordinates_full.txt', sep='\t')
    isoforms = pd.read_csv(f'{path}/app/src/isoform_list.tsv', sep='\t')


    return TRANSCRIPTS, exons, isoforms

@st.cache_data(show_spinner=False)
def get_features_dataset():
    path = os.getcwd()
    return pd.read_csv(f'{path}/app/src/features_dataset.tsv', sep='\t')


def overlapping_exons(start, end, exon):
    x, y = exon
    return not x <= start < y or x <= end < y


def plotly_isoform_structure(fig, isoform, transcript_length, exons_coord):

    # Select exons for isoform of interest
    exons_coord = exons_coord.loc[(exons_coord['Transcript stable ID'] == isoform) & (exons_coord['cDNA coding start'].notna())].sort_values('Exon rank in transcript')

    #### DRAW LINE FIRST

    # get start / end coordinates for the isoform
    transcript_start = 0
    transcript_end = transcript_length[isoform]

    # Create gene line to be plotted
    fig.add_shape(type='line', x0=transcript_start, y0=0.5, x1=transcript_end, y1=0.5,
                  line=dict(color='black', width=1.5), row=1, col=1)

    #### THEN DRAW EXONS

    # Process exons
    exons_set = []

    for _, exon in exons_coord.iterrows():

        start = exon['cDNA coding start'] - 1
        end = exon['cDNA coding end']

        set_size = len(exons_set)

        if set_size == 0:
            exons_set.append((start, end))

        elif all(overlapping_exons(start, end, exons_set[n]) for n in range(set_size)):
            exons_set.append((start, end))

    strand = exons_coord['Strand'].unique()[0]
    strand_color = {1: "LightPink", -1: "LightSkyBlue"}

    length = transcript_end + transcript_end * 0.2
    arrow_size = 0.04 * length

    for i, exon in enumerate(exons_set, 1):

        start, end = exon
        length = abs(start - end)
        gene_color = strand_color[strand]

        # Exons are squared shaped
        if i < len(exons_set):
            fig.add_shape(type="rect", x0=start, y0=0, x1=end, y1=1,
                          line=dict(color="black", width=2), fillcolor=gene_color, row=1, col=1)

        # Last exon is an arrow
        elif i == len(exons_set):

            if arrow_size <= length:
                xn = end - arrow_size
                fig.add_shape(type="path", path=f' M{start},0 V1 H{xn} L{end}, 0.5 L{xn},0 Z',
                              fillcolor=gene_color, line=dict(color="black", width=2), row=1, col=1)
            else:
                fig.add_shape(type="path", path=f' M{start},0  V1 L{end},0.5 Z',
                              fillcolor=gene_color, line=dict(color="black", width=2), row=1, col=1)

    return transcript_start, transcript_end


def plot_read_features(isoform, isoform_table, transcript_length, exons_coord):

    totreads = len(isoform_table)

    if totreads <= 50:
        row_heights = [6, 4]
        height = 200
    elif 50 < totreads <= 500:
        row_heights = [2, 8]
        height = 500
    elif 500 < totreads <= 1000:
        row_heights = [1, 9]
        height = 800
    else:
        row_heights = [0.5, 9.5]
        height = 1500

    # plot setting -----------------------
    fig = make_subplots(rows=2, cols=1, row_heights=row_heights, shared_xaxes=True, vertical_spacing=0.02)
    fig.update_layout(height=height)

    # Gene structure ----------------------
    transcript_start, transcript_end = plotly_isoform_structure(fig, isoform, transcript_length, exons_coord)

    # lock y axis range on gene model subplot and remove axis/grid/etc
    fig.update_yaxes(fixedrange=True, range=[-1, 2], row=1, col=1)
    fig.update_xaxes(visible=False, showgrid=False, row=1, col=1)
    fig.update_yaxes(visible=False, showgrid=False, row=1, col=1)

    # Read features ----------------------
    start_positions = []
    end_positions = []

    for idx, row in isoform_table.iterrows():
        ymax = idx

        # offset transcriptomic start
        offset_value = int(row['transcriptomic_start'])

        # Read regions ( 5'SC, alignment, 3'SC ) -------------
        sc5_start = row['SC5'] + offset_value
        aln_start = offset_value
        aln_end = row['alignment_length'] + offset_value
        sc3_end = row['SC3'] + offset_value

        start_positions.append(sc5_start)
        end_positions.append(sc3_end)

        fig.add_trace(go.Scatter(x=[sc5_start, aln_start], y=[idx, idx], mode='lines',
                                 line=dict(color='rgba(173,216,230,0.2)'),
                                 hovertext="5' soft-clip", hoverinfo='text'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[aln_start, aln_end], y=[idx, idx], mode='lines',
                                 line=dict(color='rgba(128,128,128,0.2)'),
                                 hovertext="Alignement", hoverinfo='text'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[aln_end, sc3_end], y=[idx, idx], mode='lines',
                                 line=dict(color='rgba(255,182,193,0.2)'),
                                 hovertext="3' soft-clip", hoverinfo='text'), row=2, col=1)

        # SSP sequence ------------------------
        if row['SSP_FOUND'] == 1:
            ssp_distance = int(row['SSP_dist']) + offset_value
            ssp_size = int(row['SSP_size'])
            fig.add_trace(go.Scatter(x=[ssp_distance - ssp_size, ssp_distance], y=[idx, idx], mode='lines',
                                     line=dict(color='orange'),
                                     hovertext='SSP sequence', hoverinfo='text'), row=2, col=1)

        # SPLICE LEADER sequence ------------------
        if row['ROBUST_SL_FOUND'] == 1:
            sldist = int(row['SL_distance']) + offset_value
            slscore = int(row['SL_score'])
            fig.add_trace(go.Scatter(x=[sldist - slscore, sldist], y=[idx, idx], mode='lines',
                                     line=dict(color='#d40f2c'),
                                     hovertext='SL sequence', hoverinfo='text'), row=2, col=1)

        # HAIRPIN sequence ---------------------
        if row['HAIRPIN_FOUND'] == 1:
            s1_start = row['HAIRPIN_stem1_start'] + offset_value
            s1_end = row['HAIRPIN_stem1_end'] + offset_value

            s2_start = row['HAIRPIN_stem2_start'] + offset_value
            s2_end = row['HAIRPIN_stem2_end'] + offset_value

            fig.add_trace(go.Scatter(x=[s1_start, s1_end], y=[idx, idx], mode='lines',
                                     line=dict(color='#89e0a0'),
                                     hovertext='HAIRPIN', hoverinfo='text'), row=2, col=1)
            fig.add_trace(go.Scatter(x=[s1_end, s2_start], y=[idx, idx], mode='lines',
                                     line=dict(color='black', dash='dot'),
                                     hovertext='HAIRPIN', hoverinfo='text'), row=2, col=1)
            fig.add_trace(go.Scatter(x=[s2_start, s2_end], y=[idx, idx], mode='lines',
                                     line=dict(color='#3c9152'),
                                     hovertext='HAIRPIN', hoverinfo='text'), row=2, col=1)

    # add x and y axis labels ---------------------------------
    fig['layout']['yaxis2']['title'] = '<b>Number of reads</b>'
    fig['layout']['xaxis2']['title'] = '<b>Reference transcript bases (nt)</b>'

    # plots settings ---------------------------------
    xmin = int(np.percentile(start_positions, 5))
    xmax = int(np.percentile(end_positions, 95))
    xmax = max(xmax, transcript_end)
    length = xmax - xmin
    x_start = xmin - (0.05 * length)
    x_end = xmax + (0.05 * length)

    fig.update_layout(xaxis_range=[x_start, x_end],
                      yaxis2=dict(range=[0, ymax]),
                      width=890,
                      margin=dict(l=0, r=10, b=0, t=0))

    fig.update_yaxes(zeroline=False, showline=True, linewidth=1.2, linecolor='#36454F', mirror=True,
                     showgrid=False, gridwidth=0.5, gridcolor='lightgrey',
                     tickformat=',', ticksuffix='</b>', tickfont=dict(size=12, color='#36454F', family='Roboto'),
                     ticks="outside", tickcolor='black', ticklen=5,
                     title_font=dict(size=16, color='#36454F', family='Roboto'))

    fig.update_xaxes(zeroline=False, showline=True, linewidth=1.2, linecolor='#36454F', mirror=True,
                     showgrid=False, gridwidth=0.5, gridcolor='lightgrey',
                     tickformat=',', ticksuffix='bp', tickfont=dict(size=12, color='#36454F', family='Roboto'),
                     ticks="outside", tickcolor='black', ticklen=5,
                     title_font=dict(size=16, color='#36454F', family='Roboto'))

    fig.update_layout(plot_bgcolor="rgb(255,255,255,255)", showlegend=False)

    return isoform, fig


def chose_isoform_to_plot(gene, isoforms_table, transcript_length, exons_coord):

    table = isoforms_table[isoforms_table['gene'] == gene]

    cols = st.columns([2, 2, 4])

    with cols[0]:
        isoforms = sorted(set(table['isoform']))
        isoform = st.selectbox('**Select isoform:**', isoforms, index=0)

    with cols[1]:
        st.write('# ')
        plot_button = st.button('Generate plot')

    if plot_button:
        with st.spinner('Parsing reads'):

            print('download features table')

            feature_dataset = get_features_dataset()
            sorting_col = ['isoform', 'transcriptomic_start', 'SC5']
            isoform_features = feature_dataset[feature_dataset['isoform'] == isoform].sort_values(sorting_col, ascending=False).reset_index(drop=True)
            return plot_read_features(isoform, isoform_features, transcript_length, exons_coord)

    else:
        return None


def features_legend():

    legend_header = '<span style="font-size:150%; font-weight: bold;">Figure legend:</span>'
    st.markdown(legend_header, unsafe_allow_html=True)
    st.write('#### ')

    cols = st.columns([0.5, 0.03, 0.47])

    with cols[0]:
        legendfile = get_legend_filepath('plot2')
        header_html = "<img src='data:image/png;base64,{}' class='img-fluid' width=450>"
        st.markdown(header_html.format(img_to_bytes(legendfile)), unsafe_allow_html=True)

    with cols[2]:
        legend_txt = 'Expanded representation of read features identified for each annotated gene isoform. '

        legend_html = f'<span style="font-size:120%;">{legend_txt}</span>'
        st.markdown(legend_html, unsafe_allow_html=True)
