### LIBRAIRIES
import streamlit as st


### CONFIGURATION
st.set_page_config(
    page_title="Movie Matcher - API 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


### APP
st.markdown("""
    <div style='text-align:center;'>
        <h2>API 🚀</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")


### FASTAPI
fastapi_url = "http://localhost:4000/docs"
st.markdown(f'<iframe src="{fastapi_url}" width = "100%" height = 1000 style = "border: none;"></iframe>', unsafe_allow_html=True)

st.markdown("---")


### FOOTER
st.markdown("""
    <p style='text-align:center;'>
        Powered by <a href='https://streamlit.io/'>Streamlit</a> & <a href='https://www.justwatch.com/'>JustWatch</a>
    </p>
""", unsafe_allow_html=True)