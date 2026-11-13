from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

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

# for a single post to be shown
@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post":post,"title":"Home"},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.get("/api/posts")
def get_posts():
    return posts

@app.get("/api/posts/{post_id}")
def get_post(post_id:int):
    for post in posts: 
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message =  (
        exception.detail
        if exception.detail
        else "An error occured. Please check your request again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail":message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title":exception.status_code,
            "message":message
        },
        status_code=exception.status_code,
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request:Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail":exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title":status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message":"Invalid request. Please check your input and try again."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
