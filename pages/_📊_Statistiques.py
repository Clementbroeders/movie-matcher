### LIBRAIRIES ###
import streamlit as st
import pandas as pd
import os
import plotly.express as px

### CONFIGURATION ###
st.set_page_config(
    page_title="Movie Matcher - Statistiques",
    page_icon="📊",
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
        <h1 style="font-size: 4rem;">📊 Statistiques 📊</h1>
    """, unsafe_allow_html=True)
    
with columns[5]:
    st.write("")
    st.write("")
    if st.button(label = '🏠 Retour à l\'accueil 🏠', type = 'primary', use_container_width = True):
        st.switch_page("_🎥_Accueil.py")

st.write("---")

## STATISTIQUES ##


columns = st.columns([0.5, 0.5])
with columns[0]:
    st.subheader('🎥 Contenu des films🎥')
    subcolumns = st.columns([0.5, 0.5])
    with subcolumns[0]:
        # Dernière mise à jour #
        os_date_updated = os.path.getmtime("fastapi/src/TMDB_content.csv")
        local_tz = 'Europe/Paris'
        date_updated = pd.to_datetime(os_date_updated, unit = 's', utc = True).tz_convert(local_tz).strftime('%d/%m/%Y %H:%M:%S')
        st.metric('Mise à jour des films', date_updated)
    
        # Nombre de plateformes #
        nb_plateformes = tmdb_providers['provider_id'].nunique()
        st.metric('Nombre de plateformes en France', nb_plateformes)
    with subcolumns[1]:
        # Nombre de films #
        nb_films = tmdb_content.shape[0]
        st.metric('Nombre de films répertoriés', nb_films)
        
        # Note moyenne IMDB #
        avg_imdb = tmdb_content['vote_average'].mean()
        st.metric('Note moyenne IMDB', round(avg_imdb, 2))
    
    st.write('')
    st.subheader('📈 Filtrage collaboratif 📈')
    subcolumns = st.columns([0.5, 0.5])
    with subcolumns[0]:
        # Nombre d'avis #
        nb_avis = ratings_updated.shape[0]
        st.metric('Nombre de votes', nb_avis)
        
        # Nombre de films impactés #
        nb_films_collaborative = ratings_updated['tmdb_id'].nunique()
        st.metric('Nombre de films', nb_films_collaborative)

    with subcolumns[1]:
        # Nombre d'utilisateurs #
        nb_utilisateurs = ratings_updated['userId'].nunique()
        st.metric('Nombre d\'utilisateurs', nb_utilisateurs)

        # Nombre de votes moyen par utilisateur #
        avg_votes = nb_avis / nb_utilisateurs
        st.metric('Nombre de votes moyen par utilisateur', round(avg_votes, 2))
        
with columns[1]:
    genre_count = tmdb_content['genres'].str.split(',').explode().str.strip().value_counts().sort_values(ascending=False)
    genre_count = genre_count.reset_index()
    genre_count.columns = ['Genre', 'Nombre de films']
    fig = px.bar(genre_count, x = 'Genre', y = 'Nombre de films', title = 'Nombre de films par genre', height = 600, text_auto = True)
    fig.update_layout(
        xaxis=dict(tickangle=-45),
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis_range=[-0.5, 9.5]
    )
    fig.update_layout(
        xaxis = dict(
            rangeslider = dict(visible=True),
            type = 'category'
        )
    )
    st.plotly_chart(fig)

st.write('---')

st.subheader('📊 Tableau de données 📊')
st.write('')
afficher_df = st.toggle('Cliquez pour afficher les données', False)
if afficher_df:
    st.dataframe(tmdb_content)