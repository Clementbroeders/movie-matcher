FROM continuumio/miniconda3

WORKDIR /home/app

# Install OS Dependencies
RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y

# Install Python Dependencies
COPY requirements.txt /home/app
RUN conda install -c conda-forge scikit-surprise
RUN pip install --no-cache-dir -r requirements.txt

# Download the spaCy English model
RUN python -m spacy download en_core_web_sm

# Send file to container
COPY . /home/app/

# Set the default value for the environment variable
ENV PORT=8501

# Run the Streamlit app
CMD streamlit run --server.port $PORT _🎥_Accueil.py