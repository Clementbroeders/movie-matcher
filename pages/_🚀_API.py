### LIBRAIRIES ###
import streamlit as st


### CONFIGURATION ###
st.set_page_config(
    page_title="Movie Matcher - API 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


### APP ###
st.markdown("""
    <div style='text-align:center;'>
        <h2>API 🚀</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")


### FASTAPI ###
success = False
try:
    api_urls = ['http://moviematcher-fastapi-1:4000/predict',
                'https://movie-matcher-fastapi-6b7d32444024.herokuapp.com/docs']
    for api_url in api_urls:
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                st.markdown(f'<iframe src="{fastapi_url}" width = "100%" height = 1000 style = "border: none;"></iframe>', unsafe_allow_html=True)
                success = True 
                break
        except requests.RequestException as e:
            pass
except Exception as e:
    pass
if not success:
    st.markdown("""
        <p style='text-align:center;'>
            Nous ne parvenons pas à accéder à l'API. Veuillez réessayer ultérieurement.
        </p>
    """, unsafe_allow_html=True)

st.markdown("---")


### FOOTER ###
st.markdown("""
    <p style='text-align:center;'>
        Powered by <a href='https://streamlit.io/'>Streamlit</a>, <a href='https://www.justwatch.com/'>JustWatch</a>, <a href='https://www.themoviedb.org/'>TMDB</a> & <a href='https://movielens.org/'>MovieLens</a>. © 2024 Movie Matcher.
    </p>
""", unsafe_allow_html=True)