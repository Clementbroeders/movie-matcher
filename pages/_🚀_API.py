### LIBRAIRIES ###
import streamlit as st
import requests

### CONFIGURATION ###
st.set_page_config(
    page_title="Movie Matcher - API 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

### APPLICATION ###


## HEADER ##
columns = st.columns([0.5, 1, 0.1, 0.3, 0.1])

with columns[1]:
    st.markdown("""
    <div style='text-align:center;'>
        <h1 style="font-size: 4rem;">🚀 API 🚀</h1>
    """, unsafe_allow_html=True)
    
with columns[3]:
    st.write("")
    st.write("")
    if st.button(label = 'Retour à l\'accueil', type = 'primary', use_container_width = True):
        st.switch_page("_🎥_Accueil.py")

st.write("---")


### FASTAPI ###
available_link = False
api_urls = [
    'http://movie-matcher-fastapi-1:4000',
    'https://moviematcher-fastapi.onrender.com/docs',
]
for api_url in api_urls:
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            if api_url == 'http://movie-matcher-fastapi-1:4000':
                available_link = 'http://localhost:4000/docs'
            else:
                available_link = api_url
            break
    except requests.RequestException as e:
        pass

if available_link:
    st.markdown(f'<iframe src="{available_link}" width="100%" height="1000" style="border: none;"></iframe>', unsafe_allow_html=True)
else:
    st.markdown("""
        <p style='text-align:center;'>
            Nous ne parvenons pas à accéder à l'API. Veuillez rafraichir la page ou réessayer ultérieurement.
        </p>
    """, unsafe_allow_html=True)

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