# Build image
docker build -t streamlit .

# Run container
docker run -it -v "$(pwd):/home/app" -p 8501:8501 streamlit