### LIBRAIRIES ###
import streamlit as st
import pandas as pd
import requests


### CONFIGURATION ###
st.set_page_config(
    page_title="Movie Matcher",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed"
)


### IMPORT FICHIERS ###
@st.cache_data
def load_tmdb_content():
    tmdb_content = pd.read_csv("data/TMDB_content.csv")
    return tmdb_content
tmdb_content = load_tmdb_content()
filtered_tmdb_content = load_tmdb_content()


@st.cache_data
def load_tmdb_providers():
    tmdb_providers = pd.read_csv("data/TMDB_providers.csv")
    return tmdb_providers
tmdb_providers = load_tmdb_providers()


### SESSION STATE ###
if 'filtered_tmdb_content' not in st.session_state:
    st.session_state.filtered_tmdb_content = tmdb_content.copy()

if 'recommended_movies' not in st.session_state:
    st.session_state.recommended_movies = None
    st.session_state.recommandation = False
    st.session_state.filtered_recommended_movies = None
    
if 'filtered_tmdb_providers' not in st.session_state:
    st.session_state.filtered_tmdb_providers = tmdb_providers.copy()
    
if 'selected_filters_streaming' not in st.session_state:
    st.session_state.selected_filters_streaming = {}
    
if 'selected_filters' not in st.session_state:
    st.session_state.selected_filters = {}

### FONCTIONS ###

def apply_filters(df, filters):
    filtered_df = df.copy()

    if filters:
        for filter_name, filter_values in filters.items():
            if filter_values:
                try:
                    filtered_df[filter_name] = filtered_df[filter_name].fillna('')
                    filter_conditions = [filtered_df[filter_name].str.contains(value, case=False) for value in filter_values]
                    combined_condition = pd.concat(filter_conditions, axis=1).any(axis=1)
                    filtered_df = filtered_df[combined_condition]
                except AttributeError:
                    return filtered_df.head(0)
                    
        filtered_df.reset_index(drop=True, inplace=True)
    
    return filtered_df

def calculate_column_ratios(nb_rows):
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


### HEADER ###
left_col, center_col, right_col = st.columns([1, 1, 1])
image_path = "img/dark.jpg"
with center_col: 
    st.image(image_path, use_column_width="auto")


### APP ###

## INTRODUCTION ###
st.markdown("""
    <div style='text-align:center;'>
        <p style="font-size: 1.2rem;">Bienvenue sur Movie Matcher, votre destination privilégiée pour des recommandations cinématographiques.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")


## SELECTION DES FILMS ###
st.markdown("""
    <div style='text-align:center;'>
        <h2>🌟 Votre sélection cinéphile 🌟</h2>
        <p style="font-size: 1.2rem;">Choisissez jusqu'à 5 films que vous avez appréciés, et nous vous suggérerons une sélection de films qui pourraient vous plaire.</p>
    </div>
""", unsafe_allow_html=True)

tmdb_selection = tmdb_content.loc[:,['tmdb_id', 'title']]
tmdb_selection.loc[-1] = [None, 'Selectionnez un film']
tmdb_selection.index = tmdb_selection.index + 1
tmdb_selection = tmdb_selection.sort_index()
tmdb_selection = tmdb_selection.sort_values(by='title', key=lambda x: x.replace('Selectionnez un film', ''))

columns = st.columns(5)
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

st.markdown("")
st.markdown("")

## Bouton recommandations ##
columns = st.columns([2, 1, 2])
with columns[1]:
    button_recommandations = st.button("🤖 Générer les recommandations 🤖", help = "Cliquez ici pour générer les recommandations", type = 'primary')

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
        url = 'http://docker-fastapi-1:4000/predict'
        # url = 'https://movie-matcher-fastapi-6b7d32444024.herokuapp.com/predict'
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        data = {'favorite_movies': selected_movies_list}
        response = requests.post(url, headers=headers, json=data)
        result_movies = pd.DataFrame(response.json())
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
    st.dataframe(st.session_state.recommended_movies)
    
st.markdown("---")


### FILTRES ###
st.markdown("""
    <div style='text-align:center;'>
        <h2>🔍 Votre sélection filtrée 🔍</h2>
        <p style="font-size: 1.2rem;">Nous vous recommandons de commencer par explorer les recommandations sans appliquer de filtres.</p>
        <p style="font-size: 1.2rem;">Affinez ensuite votre choix en explorant divers filtres pour trouver le film qui correspond parfaitement à vos préférences.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("")

## Initialisation des filtres ##
if st.session_state.recommandation:
    filters_genres = st.session_state.recommended_movies['genres'].str.split(',').explode('genres').str.strip().sort_values().unique() 
    filters_keywords = st.session_state.recommended_movies['keywords'].dropna().str.split(',').explode('keywords').str.strip().sort_values().unique()
    filters_year = st.session_state.recommended_movies['year'].sort_values(ascending = False).unique()
    filters_cast = st.session_state.recommended_movies['cast'].dropna().str.split(',').explode('cast').str.strip().sort_values().unique()
    filters_director = st.session_state.recommended_movies['director'].sort_values().unique()
    
else:
    filters_genres = st.session_state.filtered_tmdb_content['genres'].str.split(',').explode('genres').str.strip().sort_values().unique() 
    filters_keywords = st.session_state.filtered_tmdb_content['keywords'].dropna().str.split(',').explode('keywords').str.strip().sort_values().unique()
    filters_year = st.session_state.filtered_tmdb_content['year'].sort_values(ascending = False).unique()
    filters_cast = st.session_state.filtered_tmdb_content['cast'].dropna().str.split(',').explode('cast').str.strip().sort_values().unique()
    filters_director = st.session_state.filtered_tmdb_content['director'].sort_values().unique()

filters_streaming = st.session_state.filtered_tmdb_providers['provider_name'].sort_values().unique()

## Filtres column 1 ##

columns = st.columns(3)
with columns[0]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Genres</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters['genres'] = st.multiselect('Sélectionnez le(s) genre(s)', filters_genres, key = 'filter_genres')
    st.write("List : selected_options_genres", st.session_state.selected_filters['genres'])
    
with columns[1]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Mots-clés</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters['keywords'] = st.multiselect('Sélectionnez le(s) mot(s)-clé(s)', filters_keywords, key = "filter_keywords")
    st.write("List : selected_options_keywords", st.session_state.selected_filters['keywords'])
    
with columns[2]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Années</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters['year'] = st.multiselect('Sélectionnez l\'année ou les années', filters_year, key = "filter_year")
    st.write("List : selected_options_year", st.session_state.selected_filters['year'])

st.markdown("")
st.markdown("")

## Filtres column 2 ##

columns = st.columns(3)
with columns[0]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Acteurs</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters['cast'] = st.multiselect('Sélectionnez le(s) acteur(s)', filters_cast, key = "filter_cast")
    st.write("List : selected_options_cast", st.session_state.selected_filters['cast'])
    
with columns[1]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Réalisateur</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters['director'] = st.multiselect('Sélectionnez le réalisateur', filters_director, key = "filter_director")
    st.write("List : selected_options_director", st.session_state.selected_filters['director'])
    
with columns[2]:
    st.markdown("""
        <div style='text-align:center;'>
            <p style="font-size: 1.2rem;">Plateformes de streaming</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_filters_streaming = st.multiselect('Sélectionnez le(s) plateforme(s) de streaming', filters_streaming, key = "filter_streaming")
    st.write("List : selected_options_streaming", st.session_state.selected_filters_streaming)
    
    
## Application des filtres ##

st.write("st.session_state.selected_filters", st.session_state.selected_filters)

st.markdown("")
st.markdown("")

st.markdown("---")


### AFFICHER FILMS ###
columns = st.columns([3, 1, 3])
with columns[1]:
    button_affichage = st.button("🎥 Afficher les films 🎥", help = "Cliquez ici pour afficher les films recommandés", type = 'primary')

if button_affichage:
    ## Application des filtres ##
    if st.session_state.recommandation:
        if st.session_state.selected_filters or all(not st.session_state.selected_filters[key] for key in st.session_state.selected_filters):
            st.session_state.filtered_recommended_movies = apply_filters(st.session_state.recommended_movies, st.session_state.selected_filters)
            nb_rows = len(st.session_state.filtered_recommended_movies)
            st.dataframe(st.session_state.filtered_recommended_movies)
            st.write('st.session_state.recommandation', st.session_state.recommandation)

    elif not st.session_state.recommandation:
        if st.session_state.selected_filters or all(not st.session_state.selected_filters[key] for key in st.session_state.selected_filters):
            st.session_state.filtered_tmdb_content = apply_filters(tmdb_content, st.session_state.selected_filters)
            nb_rows = len(st.session_state.filtered_tmdb_content)
            st.write('st.session_state.recommandation tmdb with filter', st.session_state.recommandation)
        else:
            nb_rows = len(st.session_state.filtered_tmdb_content)
            st.write('st.session_state.recommandation tmdb without filter', st.session_state.recommandation)
            
    ## Affichage films recommandes ##
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
        
        poster_url_begin = "https://image.tmdb.org/t/p/w500/"
        
        ## Affichage titre films ##
        if nb_rows >= 5:
            columns = st.columns(5)
            columns_range = [i for i in range(0, 5)]
        else:
            columns = st.columns(calculate_column_ratios(nb_rows))
            columns_range = [i for i in range(1, nb_rows + 1)]
            
        for i in columns_range:
            col = columns[i]
            if nb_rows >= 5:
                movie_name = st.session_state.filtered_recommended_movies['title'][i]
            else:
                movie_name = st.session_state.filtered_recommended_movies['title'][i-1]
            col.markdown(f"""
                <div style='text-align:center;'>
                    <p style="font-size: 1rem;">{movie_name}</p>
                </div>
            """, unsafe_allow_html=True)
        
        ## Affichage posters films ##
        if nb_rows >= 5:
            columns = st.columns(5)
            columns_range = [i for i in range(0, 5)]
        else:
            columns = st.columns(calculate_column_ratios(nb_rows))
            columns_range = [i for i in range(1, nb_rows + 1)]
            
        for i in columns_range:
            col = columns[i]
            if nb_rows >= 5:
                full_poster_url = poster_url_begin + st.session_state.filtered_recommended_movies['poster_path'][i]
            else:
                full_poster_url = poster_url_begin + st.session_state.filtered_recommended_movies['poster_path'][i-1]
            col.image(full_poster_url, use_column_width="auto")
            
        ## Affichage streaming films ##
        if nb_rows >= 5:
            columns = st.columns(5)
            columns_range = [i for i in range(0, 5)]
        else:
            columns = st.columns(calculate_column_ratios(nb_rows))
            columns_range = [i for i in range(1, nb_rows + 1)]
            
        for i in columns_range:
            col = columns[i]
            col.markdown(f"""
                <div style='text-align:center;'>
                    <p style="font-size: 1rem;">Plateforme de streaming :</p>
                </div>
            """, unsafe_allow_html=True)
            
            if nb_rows >= 5:
                col.write(st.session_state.filtered_recommended_movies['watch_providers'][i])
            else:
                col.write(st.session_state.filtered_recommended_movies['watch_providers'][i-1])

st.markdown("---")


### FOOTER ###
st.markdown("""
    <p style='text-align:center;'>
        Powered by <a href='https://streamlit.io/'>Streamlit</a> & <a href='https://www.justwatch.com/'>JustWatch</a>
    </p>
""", unsafe_allow_html=True)