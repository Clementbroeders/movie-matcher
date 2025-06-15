### LIBRAIRIES ###
import streamlit as st
import pandas as pd

### CONFIGURATION ###
st.set_page_config(
    page_title="Movie Matcher - Informations films",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


### IMPORT FICHIERS ###
@st.cache_data
def load_tmdb_content():
    tmdb_content = pd.read_csv("fastapi/src/TMDB_content.csv")
    return tmdb_content
tmdb_content = load_tmdb_content()

@st.cache_data
def load_tmdb_providers():
    tmdb_providers = pd.read_csv("fastapi/src/TMDB_providers.csv")
    return tmdb_providers
tmdb_providers = load_tmdb_providers()

@st.cache_data
def load_ratings_updated():
    ratings_updated = pd.read_csv("fastapi/src/Movielens_ratings_updated.csv")
    return ratings_updated
ratings_updated = load_ratings_updated()

@st.cache_data
def load_content_based():
    content_based = pd.read_csv("fastapi/src/TMDB_content_based.csv")
    return content_based
content_based = load_content_based()


### SESSION STATE ###
if 'filtered_tmdb_content' not in st.session_state:
    st.session_state.filtered_tmdb_content = tmdb_content.copy()
    

### APPLICATION ###

## HEADER ##
columns = st.columns([0.1, 0.3, 0.1, 1, 0.1, 0.3, 0.1])

with columns[1]:
    st.write("")
    st.write("")
    if st.button(label = '🔄 Rafraichir la page 🔄', type = 'primary', use_container_width = True):
        st.rerun()

with columns[3]:
    st.markdown("""
    <div style='text-align:center;'>
        <h1 style="font-size: 4rem;">🎞️ INFORMATIONS FILMS 🎞️</h1>
    """, unsafe_allow_html=True)
    
with columns[5]:
    st.write("")
    st.write("")
    if st.button(label = '🏠 Retour à l\'accueil 🏠', type = 'primary', use_container_width = True):
        st.switch_page("_🎥_Accueil.py")

st.write("---")

## SELECTION DU FILM OU DE LA SERIE ##
columns = st.columns([0.15, 0.05, 0.6, 0.05, 0.15])
with columns[0]:
    filter_title = st.selectbox("Sélectionnez un film ou une série", tmdb_content["title_fr"], key = "filter_title")
    filtered_tmdb_content = tmdb_content[tmdb_content["title_fr"] == filter_title]
with columns[2]:
    st.markdown(f"""
        <div style='text-align:center;'>
            <h2 style="font-size: 2.5rem;">{filter_title}</h2>
        """, unsafe_allow_html=True)
with columns[4]:
    score_imdb = filtered_tmdb_content["score_imdb"].values[0].round(1)
    st.metric(label = "Note IMDB", value = score_imdb)
st.write("---")

columns = st.columns([0.75, 0.25])
with columns[0]: 
    subcolumns = st.columns([0.25, 0.75])
    with subcolumns[0]:
        st.subheader("🎬 Réalisateur 🎬")
    with subcolumns[1]:
        st.write("")
        st.write(filtered_tmdb_content["director"].values[0])
    st.write("---")
    
    subcolumns = st.columns([0.25, 0.75])
    with subcolumns[0]:
        st.subheader("🎭 Acteurs 🎭")
    with subcolumns[1]:
        st.write("")
        st.write(filtered_tmdb_content["cast"].values[0])
    st.write("---")
    
    subcolumns = st.columns([0.25, 0.75])
    with subcolumns[0]:
        st.subheader("🎞️ Genres 🎞️")
    with subcolumns[1]:
        st.write("")
        st.write(filtered_tmdb_content["genres"].values[0])
    st.write("---")
    
    subcolumns = st.columns([0.25, 0.75])
    with subcolumns[0]:
        st.subheader("🔍 Mots-clés 🔍")
    with subcolumns[1]:
        st.write("")
        st.write(filtered_tmdb_content["keywords"].values[0])
    st.write("---")

    watch_providers = filtered_tmdb_content['watch_providers'].values[0]
    subcolumns = st.columns([0.25, 0.75])
    with subcolumns[0]:
        st.subheader("📱 Plateformes de streaming 📱")
    try:
        providers_list = tmdb_providers[tmdb_providers['provider_id'].astype(int).isin([int(provider_id.strip('"')) for provider_id in watch_providers.split(',')])]['provider_name'].to_list()
        providers_list_updated = ', '.join(providers_list)
        with subcolumns[1]:
            st.write("")
            st.write(providers_list_updated)
    except AttributeError:
        if pd.isna(watch_providers):
            with subcolumns[1]:
                st.write("")
                st.error("Aucun streaming en abonnement disponible")
        else:
            providers_list = tmdb_providers[tmdb_providers['provider_id'].astype(int) == int(watch_providers)]['provider_name'].to_list()
            providers_list_updated = ', '.join(providers_list)
            with subcolumns[1]:
                st.write("")
                st.write(providers_list_updated)
    except Exception as e:
        with subcolumns[1]:
            st.write("")
            st.error("Aucun streaming en abonnement disponible")
    
    
with columns[1]:
    poster_url_begin = "https://image.tmdb.org/t/p/original"
    full_poster_url = poster_url_begin + filtered_tmdb_content["poster_path"].values[0]
    st.image(full_poster_url, use_container_width = True)
    