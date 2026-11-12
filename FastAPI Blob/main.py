from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#app object that we use to define our routes
app = FastAPI()

# to access any file of the static folder in /static in browser
app.mount("/static",StaticFiles(directory="static"), name="static")

#creating a templates obj which looks in our Template directory
templates = Jinja2Templates(directory="Templates")

posts: list[dict] =[
    {
        "id" : 1,
        "author" : "Corey Schafer",
        "title" : "FastAPI is Awesome",
        "content" : "This Framework is really easy to use and super fast.",
        "date_posted" : "April 20, 2025",
    },
    {
        "id" : 2,
        "author" : "Raj Shamani",
        "title" : "Welcome to our Podcast",
        "content" : "Taking about how to fix the tissue issue",
        "date_posted" : "November 12, 2026",
    },
    {
        "id" : 3,
        "author" : "Kamlesh",
        "title" : "Trending",
        "content" : "Instagram feed is not good these days.",
        "date_posted" : "November 7, 2026",
    },
]


#creating route
#include in schema to keep this page out of our API docs
@app.get("/", include_in_schema=False, name="home")

# passing a request parameter for Jinja2 to access the html file
# home.html is the name of our template
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts":posts, "title": "Home"})

@app.get("/api/posts")
def get_posts():
    return posts
