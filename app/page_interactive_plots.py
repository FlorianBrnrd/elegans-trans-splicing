from app_functions import *
from tab_read_features import get_read_features_files, chose_isoform_to_plot, features_legend


def chose_gene(GENES, GENESNAME):
    _style = """<style>.css-qrbaxs {margin-bottom: 0px; min-height: 0.5rem;}</style>"""
    st.markdown(_style, unsafe_allow_html=True)

    header = '<span style="font-size:110%; font-weight: bold;">Chose gene to plot:</span>'
    st.markdown(header, unsafe_allow_html=True)

    cols = st.columns([1, 1, 0.1, 1.9])

    with cols[0]:
        choice = st.radio('Input method:', options=['Type gene name', 'Select from list'])

    #with cols[3]:
    #    st.markdown("## ")
    #    atg_option = st.checkbox('Show known ATG positions (WS270)', value=True)

    with cols[1]:
        if choice == 'Select from list':

            refgene = st.selectbox('Select:', options=GENESNAME.values())
            gene = [i for i, v in GENESNAME.items() if refgene == v][0]
            return gene, refgene

        elif choice == 'Type gene name':

            gene = st.text_input('Type name: (ex: Y105E8B.1 or lev-11)', value='lev-11')

            # CDS format
            if gene in GENES:
                refgene = GENESNAME[gene]

            # Common name
            elif gene in GENESNAME.values():
                refgene = gene
                gene = [i for i, v in GENESNAME.items() if gene == v][0]

            else:
                gene = None
                refgene = None

            st.session_state['input'] = True
            return gene, refgene

        else:
            return None, None


def legend():
    legend_header = '<span style="font-size:150%; font-weight: bold;">Figure legend:</span>'
    st.markdown(legend_header, unsafe_allow_html=True)
    st.write('## ')

    cols = st.columns([0.22, 0.03, 0.75])

    with cols[0]:
        legendfile = get_legend_filepath('plot1')
        header_html = "<img src='data:image/png;base64,{}' class='img-fluid' width=180>"
        st.markdown(header_html.format(img_to_bytes(legendfile)), unsafe_allow_html=True)

    with cols[2]:
        legend_txt = 'Each alignment start position observed was plotted at the corresponding genomic position with ' \
                     'the number of supporting reads. The dots are colored according to the observed trans-splicing ' \
                     'events with red indicating a majority of SL reads, green a majority of endogenous hairpin ' \
                     'reads and blue reads with no evidence for either. ' \
                     'Vertical dotted lines indicate known ATG positions (WormBase release WS270).'

        legend_html = f'<span style="font-size:120%;">{legend_txt}</span>'
        st.markdown(legend_html, unsafe_allow_html=True)


def display_error():
    gene_header = ("<div style=\"background: #ffe2e0; font-size: 16px; padding: 10px; border-radius: 10px; "
                   "border: 1px solid DarkRed; margin: 10px;\"><div style=\"color: darkred;\"><strong>Requested "
                   "gene plot cannot be generated.</strong></div><br />This error can appear because:<br />- The "
                   "name entered is invalid<br />- The requested gene was not detected in our sequencing "
                   "experiments.<br /><br />Please verify the informations entered and contact the authors if "
                   "necessary.</div>")

    st.markdown(gene_header, unsafe_allow_html=True)


def plot_settings():
    st.sidebar.write('### 2. Customize plot:')
    return st.checkbox('Show known ATG positions (WS270)', value=True)


def display_gene_infos(gene, refgene):

    if gene == refgene:
        gene_header = f'<div style="font-size: 20px; text-align: center;"><b>{refgene}</b></div>'
    else:
        gene_header = f'<div style="font-size: 20px; text-align: center;"><b><i>{refgene}</i> ({gene})</b></div>'

    st.markdown(gene_header, unsafe_allow_html=True)


def interactive_plots():

    # open ref files and cache them
    genes, exons, dataset, GENES, GENESNAME, ATGPOSITIONS = get_reference_files()
    transcript_length, exons_coord, feature_dataset = get_read_features_files()

    # chose gene to plot
    gene, refgene = chose_gene(GENES, GENESNAME)

    # checking gene name input
    if gene is None and refgene is None:
        display_error()

    else:

        st.write('# ')

        tab1, tab2 = st.tabs(["**1. Plot trans-splicing per positions**", "**2. Plot features detected within reads**"])

        with tab1:

            display_gene_infos(gene, refgene)

            # generate and show gene plot
            gene_plot = plot_gene_start(dataset, gene, genes, exons, ATGPOSITIONS, show_atg=True)

            config = {'displayModeBar': False}
            st.plotly_chart(gene_plot, use_container_width=False, config=config)

            # add legend below
            legend()

        with tab2:

            #result = chose_isoform_to_plot(gene, feature_dataset, transcript_length, exons_coord)
            result = None
            if result:
                isoform, features_plots = result

                if features_plots:

                    # empty container for adding name above plot after it is generated
                    cont = st.container()

                    # add spinning widgt while generating plot
                    with st.spinner('Rendering plot'):

                        # generate plot
                        config = {'displayModeBar': False}
                        st.plotly_chart(features_plots, use_container_width=False, config=config)

                        # add isoform name above plot
                        with cont:
                            isoform_header = f'<div style="font-size: 20px; text-align: center;"><b>{isoform}</b></div>'
                            st.markdown(isoform_header, unsafe_allow_html=True)

                        # show plot legend
                        st.write('# ')
                        features_legend()


if __name__ == '__main__':
    interactive_plots()
