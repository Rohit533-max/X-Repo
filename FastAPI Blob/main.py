from fastapi import FastAPI
from fastapi.responses import HTMLResponse
#app object that we use to define our routes
app = FastAPI()



students = [
    {
        "id": 1,
        "name": "Rahul Sharma",
        "email": "rahul@gmail.com",
        "age": 21,
        "course": "Computer Science",
        "city": "Chandigarh",
        "is_active": True,
        "marks": 85.5
    },
    {
        "id": 2,
        "name": "Priya Verma",
        "email": "priya@gmail.com",
        "age": 22,
        "course": "Information Technology",
        "city": "Delhi",
        "is_active": True,
        "marks": 91.0
    },
    {
        "id": 3,
        "name": "Aman Singh",
        "email": "aman@gmail.com",
        "age": 20,
        "course": "Mechanical Engineering",
        "city": "Ludhiana",
        "is_active": False,
        "marks": 76.5
    },
    {
        "id": 4,
        "name": "Neha Gupta",
        "email": "neha@gmail.com",
        "age": 23,
        "course": "Computer Science",
        "city": "Amritsar",
        "is_active": True,
        "marks": 88.0
    },
    {
        "id": 5,
        "name": "Arjun Patel",
        "email": "arjun@gmail.com",
        "age": 21,
        "course": "Data Science",
        "city": "Mumbai",
        "is_active": True,
        "marks": 79.5
    },
    {
        "id": 6,
        "name": "Simran Kaur",
        "email": "simran@gmail.com",
        "age": 22,
        "course": "Information Technology",
        "city": "Patiala",
        "is_active": False,
        "marks": 94.0
    },
    {
        "id": 7,
        "name": "Karan Mehta",
        "email": "karan@gmail.com",
        "age": 24,
        "course": "Business Administration",
        "city": "Jaipur",
        "is_active": True,
        "marks": 82.0
    },
    {
        "id": 8,
        "name": "Anjali Sharma",
        "email": "anjali@gmail.com",
        "age": 20,
        "course": "Data Science",
        "city": "Mohali",
        "is_active": True,
        "marks": 89.5
    },
    {
        "id": 9,
        "name": "Vikram Kumar",
        "email": "vikram@gmail.com",
        "age": 23,
        "course": "Computer Science",
        "city": "Jalandhar",
        "is_active": False,
        "marks": 68.0
    },
    {
        "id": 10,
        "name": "Pooja Verma",
        "email": "pooja@gmail.com",
        "age": 21,
        "course": "Information Technology",
        "city": "Delhi",
        "is_active": True,
        "marks": 92.5
    }
]


#creating route
@app.get("/", response_class=HTMLResponse)

def home():
    return f"<h1>{students[0]['name']}</h1>"
    #we are just returning a simple dictionary here, the fast api automatically convert it into JSON.

@app.get("/api/students")
def get_students():
    return students
