import streamlit as st
import pandas as pd

### Config
st.set_page_config(
    page_title="Movie Matcher",
    page_icon="🎥",
    layout="wide"
)

# API TMDB key




# Import des fichier CSV
tmdb_content = pd.read_csv("data/TMDB_content.csv")


### Header
left_col, center_col, right_col = st.columns([1, 3, 1]) # Créer un espace vide à gauche pour centrer l'image
image_path = "img/dark.jpg"
with center_col: 
    st.image(image_path, width = 800) # Charger l'image dans la colonne centrale


### App
with center_col: 
    st.markdown("""
        <p style='text-align:center;'>
        Bienvenue sur notre site internet Movie Matcher
        
        Selectionnez jusqu'à 5 films que vous avez aimés et nous vous proposerons une liste de films qui pourraient vous plaire.
        </p>
    """, unsafe_allow_html=True)

# Selection des films
# Diviser l'écran en 5 colonnes
columns = st.columns(5)
# Selectionner colonne dataframe + ajout ligne vide
tmdb_content = tmdb_content.loc[:,['TMDB_id', 'title']]
tmdb_content.loc[-1] = [None, 'Selectionner un film']
tmdb_content.index = tmdb_content.index + 1
tmdb_content = tmdb_content.sort_index()
tmdb_content = tmdb_content.sort_values(by='title', key=lambda x: x.replace('Selectionner un film', ''))

# Liste déroulante pour chaque colonne
movie_1 = columns[0].selectbox("Film 1", tmdb_content['title'])
movie_2 = columns[1].selectbox("Film 2", tmdb_content['title'])
movie_3 = columns[2].selectbox("Film 3", tmdb_content['title'])
movie_4 = columns[3].selectbox("Film 4", tmdb_content['title'])
movie_5 = columns[4].selectbox("Film 5", tmdb_content['title'])

st.markdown("---")

### Footer 
st.markdown("""
    
    Powered by [Streamlit](https://docs.streamlit.io/) & [JustWatch](https://www.justwatch.com/)
""")