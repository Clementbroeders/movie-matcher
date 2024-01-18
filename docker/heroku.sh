# Connection Heroku
heroku container:login

# Push container to Heroku
heroku container:push web -a movie-matcher-fastapi
heroku container:push web -a movie-matcher-streamlit

# Release container to Heroku
heroku container:release web -a movie-matcher-fastapi
heroku container:release web -a movie-matcher-streamlit

# Open app
heroku open -a movie-matcher-fastapi
heroku open -a movie-matcher-streamlit