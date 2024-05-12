### LIBRAIRIES ###
import streamlit as st
import random


### CONFIGURATION ###
st.set_page_config(
    page_title="Movie Matcher - Accueil",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed"
)


### HEADER ###
image_paths = {
    'light': "img/light.jpg",
    'dark': "img/dark.jpg"
}
random_theme_mode = random.choice(['light', 'dark'])

left_col, center_col, right_col = st.columns([1, 1, 1])
with center_col: 
    st.image(image_paths[random_theme_mode], use_column_width="auto")


### APPLICATION ###

## INTRODUCTION ###
st.markdown("""
    <div style='text-align:center;'>
        <p style="font-size: 1.2rem;">Bienvenue sur la page d'accueil Movie Matcher, votre destination privilégiée pour des recommandations cinématographiques.</p>
        <p style="font-size: 1.2rem;">Découvrez des films et des séries recommandés pour vous, basés sur le contenu que vous avez apprécié.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

## BOUTONS PAGE ACCUEIL
st.markdown("")

columns = st.columns([0.5, 1, 0.5, 1, 0.5])

with columns[1]:
    if st.button(label = '🎬 Découvrir des Films 🎬', type = 'primary', use_container_width = True):
        st.switch_page("pages/_🎬_Films.py")

with columns[3]:
    if st.button(label = '📺 Découvrir des Séries (à venir)📺', type = 'secondary', use_container_width = True):
        st.switch_page("pages/_📺_Séries.py")
    
st.markdown("""
    <div style='text-align:center;'>
        <p></p>
        <p style="font-size: 1.2rem;">Information : Pour le moment, uniquement les films sont disponibles</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("")
st.markdown("")

columns = st.columns([0.5, 1, 0.5, 1, 0.5])
with columns[2]:
    if st.button(label = '🚀 Afficher l\'API 🚀', type = 'primary', use_container_width = True):
        st.switch_page("pages/_🚀_API.py")

st.markdown("")
st.markdown("---")


### FOOTER ###
st.markdown("""
    <div style='text-align:center;'>
        <p>
            Powered by <a href='https://streamlit.io/'>Streamlit</a>, <a href='https://www.justwatch.com/'>JustWatch</a>, <a href='https://www.themoviedb.org/'>TMDB</a> & <a href='https://movielens.org/'>MovieLens</a>
        </p>
        <p>
            Voir le code source sur <a href='https://github.com/Clementbroeders/movie-matcher'>GitHub</a>. © 2024 Movie Matcher.
        </p>
    </div>
""", unsafe_allow_html=True)