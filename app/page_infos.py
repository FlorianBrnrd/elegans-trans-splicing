import streamlit as st


def show_title():

    txt = 'Quantitative analysis of <i>C. elegans</i> transcripts by Nanopore direct-cDNA sequencing reveals terminal ' \
          'hairpins in non trans-spliced mRNAs.'
    txt2 = 'Florian Bernard, Delphine Dargere, Oded Rechavi, Denis Dupuy.'

    legend_html = f'<span style="font-size:140%;"><b>{txt}</b></span><br><span style="font-size:110%;">{txt2}</span>'
    st.markdown(legend_html, unsafe_allow_html=True)


def show_abstract():

    st.markdown('# ')
    st.markdown('<span style="font-size:120%;"><b>Abstract:</b></span>', unsafe_allow_html=True)

    abstract = 'Nematode mRNA processing involves a trans-splicing step through which a 21bp sequenced ' \
    'from a snRNP replaces the original 5’ end of the primary transcript. It has long been held that 70% ' \
    'of *C. elegans* mRNAs are submitted to trans- splicing. Our recent work suggested that the ' \
    'mechanism is more pervasive but not fully captured by mainstream transcriptome sequencing ' \
    'methods.<br>' \
    'In this study, we used Oxford Nanopore’s long-read amplification-free sequencing technology to ' \
    'perform a comprehensive analysis of trans-splicing in worms. ' \
    'We demonstrated that spliced leader (SL) sequences presence at the 5’ end of the messengers ' \
    'affected library preparation and generated sequencing artefacts due to their self-complementarity. ' \
    'Consistent with our previous observations, we found evidence of trans- splicing for most genes. ' \
    'However, a subset of genes appears to be only marginally trans-spliced. These messengers all ' \
    'share the capacity to generate a 5’ terminal hairpin structure mimicking the SL structure providing a ' \
    'mechanistic explanation for their non conformity. Altogether, our data provides the most ' \
    'comprehensive quantitative analysis of SL usage to date in *C. elegans*.'

    abstract_html = f'<span style="font-size:100%;">{abstract}</span>'
    st.markdown(abstract_html, unsafe_allow_html=True)


def show_biorxiv():

    url = ''
    biorxiv = f'<span style="font-size:100%;">See Manuscript on <a href="{url}">Biorxiv</a>.</span>'
    st.markdown(biorxiv, unsafe_allow_html=True)


def show_contacts():


    st.markdown('---')

    dupuy_url = 'http://www.iecb.u-bordeaux.fr/teams/DUPUY/DupuylabSite/Welcome.html'
    rechavi_url = 'https://www.odedrechavilab.com/'
    txt = f"This work is a collaboration between <b><a href='{dupuy_url}'>Dupuy's Lab</a></b> and <b><a href='{rechavi_url}'>Rechavi's Lab</a></b>."
    st.markdown(txt, unsafe_allow_html=True)

    devname = """App created by <b>Florian Bernard, Ph.D</b>."""
    github = """[![Github](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/FlorianBrnrd)"""
    twitter = """[![Twitter](https://badgen.net/badge/icon/twitter?icon=twitter&label)](https://twitter.com/florianbrnrd)"""

    full = devname + """<br>""" + github + '     ' + twitter
    st.markdown(full, unsafe_allow_html=True)


def display_informations():

    show_title()

    show_abstract()

    show_biorxiv()

    show_contacts()


if __name__ == '__main__':

    display_informations()
