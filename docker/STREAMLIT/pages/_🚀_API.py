import streamlit as st

### Config
st.set_page_config(
    page_title="Movie Matcher - API 🚀",
    page_icon="🚀",
    layout="wide"
)

### App
st.title("🚀 API")

### FASTAPI

fastapi_url = "http://localhost:4000/docs"
st.markdown(f'<iframe src="{fastapi_url}" width = "100%" height = 1000 style = "border: none;"></iframe>', unsafe_allow_html=True)


### Footer 
st.markdown("""
    Powered by [Streamlit](https://docs.streamlit.io/) & [JustWatch](https://www.justwatch.com/)
""")