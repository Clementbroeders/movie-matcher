### LIBRAIRIES
import streamlit as st
import pandas as pd


### CONFIGURATION
st.set_page_config(
    page_title="Movie Matcher",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed"
)


### API TMDB KEY
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMTFkY2JjYzE4MTFlNWIxOGI3MDg1MTIyOWRiOGYzZSIsInN1YiI6IjY1OTQzNWVlY2U0ZGRjNmQ5MDdlYWQxNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.5VYKD-qYGgixOfyjsDIR5We_wmJklWml5waulWzQVTA"
}


### IMPORT FICHIERS
@st.cache_data
def load_tmdb_content():
    tmdb_content = pd.read_csv("data/TMDB_content.csv")
    return tmdb_content
tmdb_content = load_tmdb_content()


### HEADER
left_col, center_col, right_col = st.columns([1, 3, 1])
image_path = "img/dark.jpg"
with center_col: 
    st.image(image_path, use_column_width="auto")


### APP

## INTRODUCTION
st.markdown("""
    <div style='text-align:center;'>
        <p style="font-size: 1.2rem;">Bienvenue sur Movie Matcher, votre destination privilégiée pour des recommandations cinématographiques.</p>
        <p style="font-size: 20px;">Choisissez jusqu'à 5 films que vous avez appréciés, et nous vous suggérerons une sélection de films qui pourraient vous plaire.</p>
    </div>
""", unsafe_allow_html=True)


## SELECTION DES FILMS
st.markdown("""
    <div style='text-align:center;'>
        <h2>Votre sélection cinéphile</h2>
    </div>
""", unsafe_allow_html=True)

tmdb_selection = tmdb_content.loc[:,['tmdb_id', 'title']]
tmdb_selection.loc[-1] = [None, 'Selectionnez un film']
tmdb_selection.index = tmdb_selection.index + 1
tmdb_selection = tmdb_selection.sort_index()
tmdb_selection = tmdb_selection.sort_values(by='title', key=lambda x: x.replace('Selectionnez un film', ''))

columns = st.columns(5) # Selection films
selected_movies = []
for i, column in enumerate(columns):
    column.markdown(f"""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Film {i+1}</p>
        </div>
    """, unsafe_allow_html=True)
    movie = column.selectbox(f"Film {i+1}", tmdb_selection['title'], label_visibility='collapsed')
    movie_id = tmdb_selection.loc[tmdb_selection['title'] == movie, 'tmdb_id'].values[0]
    selected_movies.append({"id": movie_id, "title": movie})

st.markdown("---")


### FILTRES
st.markdown("""
    <div style='text-align:center;'>
        <h2>Votre sélection filtrée</h2>
        <p style="font-size: 1.2rem;">Nous vous recommandons de commencer par explorer les recommandations sans appliquer de filtres.</p>
        <p style="font-size: 1.2rem;">Affinez ensuite votre choix en explorant divers filtres pour trouver le film qui correspond parfaitement à vos préférences.</p>
        
    </div>
""", unsafe_allow_html=True)

columns = st.columns(3) # Filtres groupe 1
with columns[0]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Genres</p>
        </div>
    """, unsafe_allow_html=True)
    tmdb_filter_genres = tmdb_content['genres'].str.split(',').explode('genres').str.strip().sort_values().unique() # Créer une liste des genres uniques
    selected_options = st.multiselect('Sélectionnez le(s) genre(s)', tmdb_filter_genres, key = "filter_genres") # multiselect pour sélectionner plusieurs options
    
with columns[1]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Mots-clés</p>
        </div>
    """, unsafe_allow_html=True)
    tmdb_filter_keywords = tmdb_content['keywords'].dropna().str.split(',').explode('keywords').str.strip().sort_values().unique()
    selected_options = st.multiselect('Sélectionnez le(s) mot(s)-clé(s)', tmdb_filter_keywords, key = "filter_keywords")
    
with columns[2]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Années</p>
        </div>
    """, unsafe_allow_html=True)
    tmdb_filter_genres_3 = tmdb_content['genres'].str.split(',').explode('genres').unique()
    selected_options = st.multiselect('Sélectionnez l\'année ou les années', tmdb_filter_genres_3, key = "filter_annees")


columns = st.columns(3) # Filtres groupe 2
with columns[0]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Acteurs</p>
        </div>
    """, unsafe_allow_html=True)
    tmdb_filter_genres = tmdb_content['genres'].str.split(',').explode('genres').unique() # Créer une liste des genres uniques
    selected_options = st.multiselect('Sélectionnez le(s) acteur(s)', tmdb_filter_genres, key = "filter_acteurs") # multiselect pour sélectionner plusieurs options
    
with columns[1]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Réalisateur</p>
        </div>
    """, unsafe_allow_html=True)
    tmdb_filter_genres_2 = tmdb_content['genres'].str.split(',').explode('genres').unique() # Créer une liste des genres uniques
    selected_options_2 = st.multiselect('Sélectionnez le réalisateur', tmdb_filter_genres_2, key = "filter_director") # multiselect pour sélectionner plusieurs options
    
with columns[2]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Plateformes de streaming</p>
        </div>
    """, unsafe_allow_html=True)
    tmdb_filter_genres_3 = tmdb_content['genres'].str.split(',').explode('genres').unique() # Créer une liste des genres uniques
    selected_options_3 = st.multiselect('Sélectionnez le(s) plateforme(s) de streaming', tmdb_filter_genres_3, key = "filter_streaming") # multiselect pour sélectionner plusieurs options

st.markdown("---")


### RECOMMANDATIONS

columns = st.columns(9)
with columns[4]:
    button_recommandations = st.button("Recommandations 🌟", help = "Cliquez ici pour afficher les recommandations", type = 'primary')

result_container = st.empty()

if button_recommandations:
    result_container.markdown("""
        <div style='text-align:center;'>
            <h2>Nos recommandations</h2>
            <p style="font-size: 1.2rem;">Voici quelques-uns des films que nous vous recommandons.</p>
            
        </div>
    """, unsafe_allow_html=True)

    columns = st.columns(5) # Recommandations   
    for i, column in enumerate(columns):
        column.markdown(f"""
            <div style='text-align:center;'>
                <p style="font-size: 1.2rem;">Film recommandé {i+1}</p>
            </div>
        """, unsafe_allow_html=True)
        column.image("https://image.tmdb.org/t/p/w500//hr0L2aueqlP2BYUblTTjmtn0hw4.jpg", use_column_width="auto")
            
st.markdown("---")


### FOOTER
st.markdown("""
    <p style='text-align:center;'>
        Powered by <a href='https://streamlit.io/'>Streamlit</a> & <a href='https://www.justwatch.com/'>JustWatch</a>
    </p>
""", unsafe_allow_html=True)