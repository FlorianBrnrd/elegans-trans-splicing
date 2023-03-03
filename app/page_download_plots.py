import streamlit as st
import plotly.io as pio
from app_functions import plot_gene_start, get_reference_files
import os
from fpdf import FPDF


def parse_input(_input):
    if type(_input) != str:
        _input = _input.read().decode('UTF-8')
    input_list = _input.splitlines()

    input_list = list(filter(None, input_list))
    return input_list


def convert_input(input_list, GENES, GENESNAME):
    converted = []

    for gene in input_list:

        # CDS format
        if gene in GENES:
            converted.append(gene)
        # Common name
        elif gene in GENESNAME.values():
            gene = [i for i, v in GENESNAME.items() if gene == v][0]
            converted.append(gene)

    return converted


def validate_input(gene_list, GENES):
    invalid = [g for g in gene_list if g not in GENES]
    return (False, invalid) if invalid else (True, invalid)


def invalid_name_error(gene_list, container):
    if len(gene_list) > 50:
        _list = ', '.join(gene_list[:50]) + 'etc...'

    else:
        _list = ', '.join(gene_list)

    header = ("<div style=\"background: #ffe2e0; font-size: 16px; padding: 10px; border-radius: 10px; "
              "border: 1px solid DarkRed; margin: 10px;\"><div style=\"color: darkred;\"><strong>"
              f"Invalid gene name identified:</strong></div>{_list}<br />"
              "<div style=\"color: black;\"><strong><br />Please verify your input and re-start.</div>")

    container.markdown(header, unsafe_allow_html=True)


def download_plots():

    #### basic settings
    # kaleido settings
    pio.kaleido.scope.chromium_args = ("--headless", "--no-sandbox", "--single-process", "--disable-gpu")

    # get files for computation
    genes, exons, dataset, GENES, GENESNAME, ATGPOSITIONS = get_reference_files()

    #### custom css styling
    _style = """<style>.css-qrbaxs {margin-bottom: 0px; min-height: 0.5rem;}</style>"""
    st.markdown(_style, unsafe_allow_html=True)

    #### user input
    method_txt = '<span style="font-size:110%; font-weight: bold;">Select input method:</span>'
    st.markdown(method_txt, unsafe_allow_html=True)
    method = st.radio('', options=['Type gene name(s)', 'Upload from file (.txt)'])

    if method == 'Type gene name(s)':
        type_text = '<span style="font-size:110%; font-weight: bold;">Type one gene name per line:</span>'
        st.markdown(type_text, unsafe_allow_html=True)

        _input = st.text_area('', value="", height=200, max_chars=500)

    elif method == 'Upload from file (.txt)':
        upload_text = '<span style="font-size:110%;font-weight:bold;">' \
                      'Upload a .txt file (one gene name per line):</span>'

        st.markdown(upload_text, unsafe_allow_html=True)
        _input = st.file_uploader('', accept_multiple_files=False, type=['txt'])

    else:
        _input = None

    txt = '*(Only plots showing trans-splicing per positions will be generated, ' \
          'expanded features annotations are currently not available for download.)*'
    st.write(txt)

    #### validation of user input
    latest_iteration = st.empty()
    latest_iteration.markdown(' ')
    processing = st.empty()

    generate = processing.button('Validate') if _input else False

    #### processing
    if generate:

        # parse input
        gene_list = parse_input(_input)

        # convert input to CDS
        processed_list = convert_input(gene_list, GENES, GENESNAME)

        # verify it is in dataset
        valid, invalid_genes = validate_input(processed_list, GENES)

        if valid is False:
            invalid_name_error(invalid_genes, container=processing)

        else:

            # create pdf
            pdf = FPDF(format=(180, 240), orientation="landscape")

            # create progress bar
            my_bar = processing.progress(0)
            nb = len(gene_list)

            for n, refgene in enumerate(processed_list, start=0):

                common = GENESNAME[refgene]

                # update text
                titleplot = f'{common} ({refgene})' if common != refgene else str(refgene)
                percent = round(n/nb*100)
                latest_iteration.write(f'processing {titleplot} - Completed:{n}/{nb} ({percent}%)')

                # update bar
                prog = n / nb
                my_bar.progress(prog)

                gene_plot = plot_gene_start(dataset, refgene, genes, exons, ATGPOSITIONS, show_atg=True)

                fig = gene_plot.update_layout(margin=dict(l=100, r=100, b=100, t=100), title_text=titleplot,
                                              title_font_size=30, title_font_family='Roboto', title_font_color='black')

                # save file
                fig.write_image(f"fig{n}.png", width=1200, height=900, scale=2)

                # add to report
                pdf.add_page()
                pdf.image(f"fig{n}.png", x=15, y=20, h=150, w=200)

                # remove figures when added to pdf report to free space
                os.remove(f"fig{n}.png")

            # finally
            my_bar = processing.progress(100)
            latest_iteration.write(f'Completed:{nb}/{nb} (100%)')

            pdf.output('plots_archive.pdf')

            # download report
            with open('plots_archive.pdf', 'rb') as pdf_file:
                pdfbytes = pdf_file.read()

            st.download_button(label='Download file', data=pdfbytes, file_name='elegans_trans-splicing_plots.pdf',
                               mime='application/octet-stream')

            os.remove("plots_archive.pdf")


if __name__ == '__main__':
    download_plots()
