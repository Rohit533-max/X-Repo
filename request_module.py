import requests

url = "https://randomuser.me/api/"
#Fetch a random user from the API and print their name, gender, email, and country
try:
    r = requests.get(url, timeout = 5)
    r.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
    user = r.json()['results'][0]
    print("Name: ", user['name']['title'], user['name']['first'], user['name']['last'])
    print("Gender:",user['gender'])
    print("Email:", user['email'])
    print("Country:",user['location']['country'])
    


except requests.exceptions.RequestException as e:
    print("An error occured", e)


#exercise 2 : Fetch a post from https://jsonplaceholder.typicode.com/posts/5 and print its title.
try:
    r1 = requests.get("https://jsonplaceholder.typicode.com/posts/5", timeout = 5)
    r1.raise_for_status()
    post = r1.json()
    print("Post Title:", post['title'])
except requests.exceptions.RequestException as e:
    print("An error occurred while fetching the post:", e)

# exercise 3: Fetch all users from https://jsonplaceholder.typicode.com/users and print their names.
try:
    r2 = requests.get("https://jsonplaceholder.typicode.com/users", timeout = 5)
    r2.raise_for_status()
    user = r2.json()
    for users in user:
        print(users['name'])

except requests.exceptions.RequestException as e:
    print("Error occur", e)

#example 4: Send a POST request to https://httpbin.org/post with your name and age as JSON.
new_post = {
    'name': 'sergio',
    'age': 35
}

r3 = requests.post("https://httpbin.org/post",json=new_post)

print(r3.status_code)

