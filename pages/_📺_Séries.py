### LIBRAIRIES ###
import streamlit as st
import pandas as pd


### CONFIGURATION ###
st.set_page_config(
    page_title="Movie Matcher - Séries",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed"
)


### APPLICATION ###

## HEADER ##
columns = st.columns([0.5, 1, 0.1, 0.3, 0.1])

with columns[1]:
    st.markdown("""
    <div style='text-align:center;'>
        <h1 style="font-size: 4rem;">📺 SERIES 📺</h1>
    """, unsafe_allow_html=True)
    
with columns[3]:
    st.write("")
    st.write("")
    if st.button(label = '🏠 Retour à l\'accueil 🏠', type = 'primary', use_container_width = True):
        st.switch_page("_🎥_Accueil.py")

st.write("---")


## SELECTION DES SERIES ##

st.markdown("""
    <div style='text-align:center;'>
        <p style="font-size: 1.2rem;"> 🚧 Page en cours de construction 🚧 </p>
""", unsafe_allow_html=True)

st.write("---")

### FOOTER ###
st.markdown("""
    <div style='text-align:center;'>
        <p>
            Powered by <a href='https://streamlit.io/'>Streamlit</a>, <a href='https://www.justwatch.com/'>JustWatch</a>, <a href='https://www.themoviedb.org/'>TMDB</a> & <a href='https://movielens.org/'>MovieLens</a>
        </p>
        <p>
            Voir le code source sur <a href='https://github.com/Clementbroeders/movie-matcher'>GitHub</a>. © 2025 Movie Matcher.
        </p>
    </div>
""", unsafe_allow_html=True)