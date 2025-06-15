### LIBRAIRIES ###
import streamlit as st
import pandas as pd
import requests
from utils.movie_recommandation import movie_recommandation


### CONFIGURATION ###
st.set_page_config(
    page_title="Movie Matcher - Films",
    page_icon="🎬",
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

if 'recommended_movies' not in st.session_state:
    st.session_state.recommended_movies = None
    st.session_state.recommandation = False
    st.session_state.filtered_recommended_movies = None
        
if 'selected_filters_streaming' not in st.session_state:
    st.session_state.selected_filters_streaming = {}
    
if 'selected_filters' not in st.session_state:
    st.session_state.selected_filters = {}
    
if 'bouton_affichage' not in st.session_state:
    st.session_state.bouton_affichage = False

if 'next_previous' not in st.session_state:
    st.session_state.next_previous = 0


### FONCTIONS ###
def apply_filters(df, filters):
    '''
    Applique les filtres sur le DataFrame de films.
    Chaque changement de filtre applique de nouveau l'intégralité des filtres.
    Le dataframe filtered_df sera utilisé pour l'affichage des films.
    '''
    filtered_df = df.copy()

    if filters:
        for filter_name, filter_values in filters.items():
            if filter_values:
                try:
                    filtered_df[filter_name] = filtered_df[filter_name].fillna('')
                    if filter_name == 'watch_providers':
                        filter_conditions = [filtered_df[filter_name].str.contains(fr'\b{value}\b', case=True) for value in filter_values]
                    elif filter_name == 'year':
                        filter_conditions = [filtered_df[filter_name].isin([value]) for value in filter_values]
                    else:
                        filter_conditions = [filtered_df[filter_name].str.contains(value, case=False) for value in filter_values]
                    combined_condition = pd.concat(filter_conditions, axis=1).any(axis=1)
                    filtered_df = filtered_df[combined_condition]
                except AttributeError:
                    return filtered_df.head(0)
                    
        filtered_df.reset_index(drop=True, inplace=True)
    
    return filtered_df

def calculate_column_ratios(nb_rows):
    '''
    Calcule les ratios de colonnes pour l'affichage des films.
    Nombre maximum de colonnes = 5
    Si le nombre de films est inférieur à 5, les colonnes sont centrées.
    '''
    if nb_rows < 5:
        left_padding = (5 - nb_rows) / 2
        right_padding = (5 - nb_rows) / 2
        if (left_padding + right_padding) < (5 - nb_rows):
            left_padding += 0.5
        elif (left_padding + right_padding) > (5 - nb_rows):
            right_padding += 0.5
        column_ratios = [left_padding] + [1] * nb_rows + [right_padding]
        return column_ratios
    return [1] * 5


### APPLICATION ###

## HEADER ##
columns = st.columns([0.1, 0.3, 0.1, 1, 0.1, 0.3, 0.1])

with columns[1]:
    st.write("")
    st.write("")
    if st.button(label = '🔄 Rafraichir la page 🔄', type = 'primary', use_container_width = True):
        st.session_state.recommended_movies = None
        st.session_state.recommandation = False
        st.session_state.filtered_recommended_movies = None
        st.session_state.selected_filters_streaming = {}
        st.session_state.selected_filters = {}
        st.session_state.bouton_affichage = False
        st.session_state.next_previous = 0
        st.rerun()

with columns[3]:
    st.markdown("""
    <div style='text-align:center;'>
        <h1 style="font-size: 4rem;">🎬 FILMS 🎬</h1>
    """, unsafe_allow_html=True)
    
with columns[5]:
    st.write("")
    st.write("")
    if st.button(label = '🏠 Retour à l\'accueil 🏠', type = 'primary', use_container_width = True):
        st.switch_page("_🎥_Accueil.py")

st.write("---")


## SELECTION DES FILMS ###
st.markdown("""
    <div style='text-align:center;'>
        <h2>🌟 Votre sélection cinéphile 🌟</h2>
        <p style="font-size: 1.2rem;">Choisissez jusqu'à 5 films que vous avez appréciés, et nous vous suggérerons une sélection de films qui pourraient vous plaire.</p>
    </div>
""", unsafe_allow_html=True)

tmdb_selection = tmdb_content.loc[:,['tmdb_id', 'title_fr']]
tmdb_selection.loc[-1] = [None, 'Selectionnez un film']
tmdb_selection.index = tmdb_selection.index + 1
tmdb_selection = tmdb_selection.sort_index()
tmdb_selection = tmdb_selection.sort_values(by='title_fr', key=lambda x: x.replace('Selectionnez un film', ''))

columns = st.columns(5)
selected_movies = []
for i, column in enumerate(columns):
    column.markdown(f"""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Film {i+1}</p>
        </div>
    """, unsafe_allow_html=True)
    movie = column.selectbox(f"Film {i+1}", tmdb_selection['title_fr'], label_visibility='collapsed')
    movie_id = tmdb_selection.loc[tmdb_selection['title_fr'] == movie, 'tmdb_id'].values[0]
    selected_movies.append({"id": movie_id, "title_fr": movie})

st.write("")

## Bouton recommandations ##
columns = st.columns([2, 1, 2])
with columns[1]:
    button_recommandations = st.button("🤖 Générer les recommandations 🤖", help = "Cliquez ici pour générer les recommandations", type = 'primary', use_container_width = True)

if button_recommandations:
    ## FastAPI + Filtres ##
    selected_movies_list = [item["id"] for item in selected_movies if item.get("id") is not None]
    if not selected_movies_list:
        st.markdown("""
            <div style='text-align:center;'>
                <p style="font-size: 1.2rem;">La liste est vide, veuillez renseigner un où plusieurs films</p>
            </div>
        """, unsafe_allow_html=True)
    else:      
        data = {'favorite_movies': selected_movies_list}
        success = False
        try:
            api_urls = [
                'http://movie-matcher-fastapi-1:4000/predict',
                # 'https://moviematcher-fastapi.onrender.com/predict' # API très lente (+ de 20 secondes)
            ]
            headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
            for api_url in api_urls:
                try:
                    response = requests.post(api_url, headers=headers, json=data)
                    if response.status_code == 200:
                        result_movies = pd.DataFrame(response.json())
                        success = True 
                        break
                except requests.RequestException as e:
                    pass
        except Exception as e:
            pass
        if not success:
            result_movies = pd.DataFrame(movie_recommandation(data, ratings_updated, content_based))

        recommended_movies = pd.merge(result_movies, tmdb_content, on='tmdb_id', how='left')
        st.session_state.recommended_movies = recommended_movies
        st.session_state.filtered_recommended_movies = recommended_movies.copy()
        st.session_state.recommandation = True

if st.session_state.recommandation:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Les recommandations ont été générées.</p>
        </div>
    """, unsafe_allow_html=True)
    
st.write("---")


### FILTRES ###
st.markdown("""
    <div style='text-align:center;'>
        <h2>🔍 Votre sélection filtrée 🔍</h2>
        <p style="font-size: 1.2rem;">Nous vous recommandons de commencer par explorer les recommandations sans appliquer de filtres.</p>
        <p style="font-size: 1.2rem;">Affinez ensuite votre choix en explorant divers filtres pour trouver le film qui correspond parfaitement à vos préférences.</p>
    </div>
""", unsafe_allow_html=True)

st.write("")

## Initialisation des filtres ##
if st.session_state.recommandation:
    filters_genres = st.session_state.recommended_movies['genres'].str.split(',').explode('genres').str.strip().sort_values().unique() 
    filters_keywords = st.session_state.recommended_movies['keywords'].dropna().str.split(',').explode('keywords').str.strip().sort_values().unique()
    filters_year = st.session_state.recommended_movies['year'].dropna().sort_values(ascending = False).unique().astype(int)
    filters_cast = st.session_state.recommended_movies['cast'].dropna().str.split(',').explode('cast').str.strip().sort_values().unique()
    filters_director = st.session_state.recommended_movies['director'].sort_values().unique()
    filters_streaming = tmdb_providers[tmdb_providers['provider_id'].astype(str).isin(
        st.session_state.recommended_movies['watch_providers'].dropna().str.split(',').explode('watch_providers').str.strip().unique()
        )]['provider_name'].sort_values()
    
else:
    filters_genres = tmdb_content['genres'].str.split(',').explode('genres').str.strip().sort_values().unique() 
    filters_keywords = tmdb_content['keywords'].dropna().str.split(',').explode('keywords').str.strip().sort_values().unique()
    filters_year = tmdb_content['year'].dropna().sort_values(ascending = False).unique().astype(int)
    filters_cast = tmdb_content['cast'].dropna().str.split(',').explode('cast').str.strip().sort_values().unique()
    filters_director = tmdb_content['director'].sort_values().unique()
    filters_streaming = tmdb_providers[tmdb_providers['provider_id'].astype(str).isin(
        tmdb_content['watch_providers'].dropna().str.split(',').explode('watch_providers').str.strip().unique()
        )]['provider_name'].sort_values()

columns = st.columns(3)
with columns[0]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Genres</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters['genres'] = st.multiselect('Sélectionnez le(s) genre(s)', filters_genres, key = 'filter_genres')
    
with columns[1]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Mots-clés</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters['keywords'] = st.multiselect('Sélectionnez le(s) mot(s)-clé(s)', filters_keywords, key = "filter_keywords")
    
with columns[2]:
    sub_columns = st.columns([0.15, 1, 0.15])
    with sub_columns[1]:
        st.markdown("""
            <div style='text-align:center;'>
                <p style="font-size: 1.2rem;">Période de sortie</p>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.selected_filters['year'] = st.slider("Sélectionnez une période", min(filters_year), max(filters_year), (min(filters_year), max(filters_year)), key = "filter_year")
        if st.session_state.selected_filters['year'][0] == min(filters_year) and st.session_state.selected_filters['year'][1] == max(filters_year):
            st.session_state.selected_filters['year'] = []
        else:
            st.session_state.selected_filters['year'] = list(range(st.session_state.selected_filters['year'][0], st.session_state.selected_filters['year'][1] + 1))

st.write("")

## Filtres column 2 ##

columns = st.columns(3)
with columns[0]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Acteurs</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters['cast'] = st.multiselect('Sélectionnez le(s) acteur(s)', filters_cast, key = "filter_cast")
    
with columns[1]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Réalisateur</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters['director'] = st.multiselect('Sélectionnez le réalisateur', filters_director, key = "filter_director")
    
with columns[2]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Plateformes de streaming</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters['watch_providers'] = st.multiselect('Sélectionnez le(s) plateforme(s) de streaming', filters_streaming, key = "filter_streaming")
    st.session_state.selected_filters['watch_providers'] = tmdb_providers[tmdb_providers['provider_name'].isin(st.session_state.selected_filters['watch_providers'])]['provider_id'].astype(str).tolist()
    
st.write("")
st.write("---")


### AFFICHER FILMS ###
columns = st.columns([1.25, 1, 1.25])
with columns[1]:
    button_affichage = st.button("🎥 Afficher les films 🎥", help = "Cliquez ici pour afficher les films recommandés", type = 'primary', use_container_width = True)
    if button_affichage:
        st.session_state.bouton_affichage = True
        st.session_state.next_previous = 0

    
if st.session_state.bouton_affichage:   
    ## Application des filtres ##
    if st.session_state.recommandation:
        if st.session_state.selected_filters or all(not st.session_state.selected_filters[key] for key in st.session_state.selected_filters):
            st.session_state.filtered_recommended_movies = apply_filters(st.session_state.recommended_movies, st.session_state.selected_filters)
            nb_rows = len(st.session_state.filtered_recommended_movies)
            
        data_affichage = st.session_state.filtered_recommended_movies

    elif not st.session_state.recommandation:
        if st.session_state.selected_filters or all(not st.session_state.selected_filters[key] for key in st.session_state.selected_filters):
            st.session_state.filtered_tmdb_content = apply_filters(tmdb_content, st.session_state.selected_filters)
            nb_rows = len(st.session_state.filtered_tmdb_content)

        else:
            nb_rows = len(st.session_state.filtered_tmdb_content)
            
        data_affichage = st.session_state.filtered_tmdb_content
    
    ## Affichage films recommandés ##
    if nb_rows == 0:
        st.markdown("""
            <div style='text-align:center;'>
                <h2>🎞️ Nos recommandations 🎞️</h2>
                <p style="font-size: 1.2rem;">Aucun film disponible. Veuillez relancer la recommandation ou retirer des filtres.</p>
            </div>
        """, unsafe_allow_html=True)    
        
    else:
        st.markdown("""
            <div style='text-align:center;'>
                <h2>🎞️ Nos recommandations 🎞️</h2>
                <p style="font-size: 1.2rem;">Voici quelques-uns des films que nous vous recommandons.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        
        ## Boutons suivants/précédents ##
        data_affichage_updated = data_affichage # Initialisation variable
        nb_rows_updated = len(data_affichage_updated) # Initialisation variable

        columns = st.columns([1, 0.25, 0.1, 0.25, 1])
                
        with columns[1]:
            if st.button(label='Précédent', type='primary', use_container_width=True):
                if st.session_state.next_previous % 5 != 0:
                    st.session_state.next_previous -= st.session_state.next_previous % 5
                else:
                    st.session_state.next_previous -= 5
                if st.session_state.next_previous < 0:
                    st.session_state.next_previous = 0
                data_affichage_updated = data_affichage.iloc[st.session_state.next_previous:].reset_index(drop=True)
                nb_rows_updated = len(data_affichage_updated)
                
        with columns[3]:
            if st.button(label='Suivant', type='primary', use_container_width=True):
                if nb_rows - st.session_state.next_previous > 5:
                    st.session_state.next_previous += 5
                    if st.session_state.next_previous > nb_rows:
                        st.session_state.next_previous = nb_rows
                    data_affichage_updated = data_affichage.iloc[st.session_state.next_previous:].reset_index(drop=True)
                    nb_rows_updated = len(data_affichage_updated)
                else:
                    data_affichage_updated = data_affichage.iloc[st.session_state.next_previous:].reset_index(drop=True)
                    nb_rows_updated = len(data_affichage_updated)
                                    
        if nb_rows_updated == nb_rows:
            st.session_state.next_previous = 0 # Réinitialisation de la variable next_previous quand un filtre est appliqué/actualisation partielle de la page  
                        
        ## Affichage titre films ##
        if nb_rows_updated >= 5:
            columns = st.columns(5)
            columns_range = [i for i in range(0, 5)]
        else:
            columns = st.columns(calculate_column_ratios(nb_rows_updated))
            columns_range = [i for i in range(1, nb_rows_updated + 1)]
            
        for i in columns_range:
            col = columns[i]
            if nb_rows_updated >= 5:
                movie_name = data_affichage_updated['title_fr'][i]
            else:
                movie_name = data_affichage_updated['title_fr'][i-1]
            col.markdown(f"""
                <div style='text-align:center;'>
                    <p style="font-size: 1rem;">{movie_name}</p>
                </div>
            """, unsafe_allow_html=True)
        
        ## Affichage posters films ##
        poster_url_begin = "https://image.tmdb.org/t/p/original"
        
        if nb_rows_updated >= 5:
            columns = st.columns(5)
            columns_range = [i for i in range(0, 5)]
        else:
            columns = st.columns(calculate_column_ratios(nb_rows_updated))
            columns_range = [i for i in range(1, nb_rows_updated + 1)]
            
        for i in columns_range:
            col = columns[i]
            if nb_rows_updated >= 5:
                full_poster_url = poster_url_begin + data_affichage_updated['poster_path'][i]
            else:
                full_poster_url = poster_url_begin + data_affichage_updated['poster_path'][i-1]
            col.image(full_poster_url, use_container_width = True)
            
        ## Affichage streaming films ##
        if nb_rows_updated >= 5:
            columns = st.columns(5)
            columns_range = [i for i in range(0, 5)]
        else:
            columns = st.columns(calculate_column_ratios(nb_rows_updated))
            columns_range = [i for i in range(1, nb_rows_updated + 1)]
            
        for i in columns_range:
            col = columns[i]
            col.markdown(f"""
                <div style='text-align:center;'>
                    <p style="font-size: 1rem;">Plateforme de streaming :</p>
                </div>
            """, unsafe_allow_html=True)
                      
            if nb_rows_updated >= 5:
                cell = f'{i}'
            else:
                cell = f'{i-1}'
                
            cell = int(cell)
            watch_providers = data_affichage_updated['watch_providers'][cell]
            
            try:
                providers_list = tmdb_providers[tmdb_providers['provider_id'].astype(int).isin([int(provider_id.strip('"')) for provider_id in watch_providers.split(',')])]['provider_name'].to_list()
                providers = ''
                for provider in providers_list:
                    providers += "- " + provider + "\n"
                col.markdown(providers)
                
            except AttributeError:
                if pd.isna(watch_providers):
                    col.markdown(f"""
                        <div style='text-align:center;'>
                            <p style="font-size: 1rem;">Aucun streaming en abonnement disponible</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    providers_list = tmdb_providers[tmdb_providers['provider_id'].astype(int) == int(watch_providers)]['provider_name'].to_list()
                    providers = ''
                    for provider in providers_list:
                        providers += "- " + provider + "\n"
                    col.markdown(providers)
                    
            except Exception as e:
                col.markdown(f"""
                    <div style='text-align:center;'>
                        <p style="font-size: 1rem;">Aucun streaming en abonnement disponible</p>
                    </div>
                """, unsafe_allow_html=True)


st.write("---")


### FOOTER ###
st.markdown("""
    <div style='text-align:center;'>
        <p>
            Propulsé par <a href='https://streamlit.io/'>Streamlit</a>, <a href='https://www.justwatch.com/'>JustWatch</a>, <a href='https://www.themoviedb.org/'>TMDB</a> & <a href='https://movielens.org/'>MovieLens</a>
        </p>
        <p>
            Voir le code source sur <a href='https://github.com/Clementbroeders/movie-matcher'>GitHub</a>. © 2025 Movie Matcher.
        </p>
    </div>
""", unsafe_allow_html=True)