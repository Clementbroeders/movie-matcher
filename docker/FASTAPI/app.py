import uvicorn
import pandas as pd 
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index():

    message = "Bienvenue sur notre API. Ce '/' est l'endpoint le plus simple et celui par défaut. Si vous voulez en savoir plus, consultez la documentation de l'api à '/docs'"

    return message

@app.get("/custom-greetings")
async def custom_greetings(name: str = "Mr (or Miss) Nobody"):
    greetings = {
        "Message": f"Hello {name} How are you today?"
    }
    return greetings

@app.get("/blog-articles/{blog_id}")
async def read_blog_article(blog_id: int):

    articles = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/articles.csv")
    if blog_id > len(articles):
        response = {
            "msg": "We don't have that many articles!"
        }
    else:
        article = articles.iloc[blog_id, :]
        response = {
            "title": article.title,
            "content": article.content, 
            "author": article.author
        }

    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) # Here you define your web server to run the `app` variable (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)