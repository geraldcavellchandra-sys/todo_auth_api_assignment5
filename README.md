# Todo List API with JWT Authentication Assignment 5

This project is an enhanced version of the previous assignment 3, updated to include **Authentication and Authorization** using **JWT (JSON Web Tokens)**.

Users must register and log in to obtain a token before accessing protected endpoints such as creating, updating, or deleting todo items.

---

## Project Description

The **Todo List API** allows users to securely manage personal tasks. The API now includes:

- User Authentication (Register + Login)
- JWT Token handling
- Authorization to ensure only the owner can modify their data
- CRUD operations for todos

Supported actions:

- Add todo items
- View your todos
- Update existing todos
- Delete todos

---

## Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python 3.x | Base programming language |
| Flask | Web framework |
| Flask-JWT-Extended | Authentication & token management |
| Werkzeug | Password hashing |
| Postman | API testing |
| JSON Files | Simple persistent storage |

---

## API Endpoints

Below is the list of available API endpoints in this project, including their HTTP method, authentication requirement, and purpose.

---------------------------------------------------------
Authentication (No Token Required)
---------------------------------------------------------

POST    /register      → Register a new user account  
POST    /login         → Login and receive a JWT access token  

---------------------------------------------------------
Todo Management (Requires Bearer Token)
---------------------------------------------------------

GET     /todos         → Retrieve all todo items belonging to the logged-in user  
POST    /todos         → Create a new todo item  
PUT     /todos/<id>    → Update an existing todo item (only if the user owns it)  
DELETE  /todos/<id>    → Delete a todo item (only if the user owns it)  

---------------------------------------------------------
Notes:
---------------------------------------------------------
- All `/todos` endpoints require a valid JWT token.
- Tokens must be added in Postman under:

Authorization → Type: Bearer Token → Paste the token


## Setup Instructions and Example (Using Postman)

Follow these steps in order to successfully run and test the authenticated Todo API.

---------------------------------------------------------
1. Create Data Files (Required Before Running the API)
---------------------------------------------------------

In the project folder, create the two required JSON files by running:

echo {} > users.json
echo {} > todos.json

(These act as simple persistent storage files.)

Both files must contain:

{}

---------------------------------------------------------
2. Start the API Server
---------------------------------------------------------

Run the Flask application:

python app.py

If successful, the terminal should show:

 * Running on http://127.0.0.1:5000

Keep this running.

---------------------------------------------------------
3. Register a New User Account
---------------------------------------------------------

Method: POST  
URL: http://127.0.0.1:5000/register  
Body → raw → JSON:

{
  "username": "richard",
  "password": "password123"
}

Expected Response: **201 Created**

{
    "message": "User registered successfully"
}

---------------------------------------------------------
4. Login to Generate JWT Token
---------------------------------------------------------

Method: POST  
URL: http://127.0.0.1:5000/login  
Body → raw → JSON:

{
  "username": "richard",
  "password": "password123"
}

Expected Response: **200 OK**
There will be a code like this 
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2NDg2MzcwOCwianRpIjoiZjMyMmJjMjAtM2I4Yy00MzFkLWEwMDMtNTI1ZWVmODYyYmRjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJpY2hhcmQiLCJuYmYiOjE3NjQ4NjM3MDgsImNzcmYiOiIzOTUwYTc1OS0xZGRlLTRjMzQtOGZkZi0zOGE3YTljZDcwYzIiLCJleHAiOjE3NjQ4NjQ2MDh9.TktZm7ydeYEQkGpiHEN14kuc76ZOV7DzlaAck936JNw"
}

Copy the `"access_token"` from the response.

---------------------------------------------------------
5. Apply Token to Authorization Header
---------------------------------------------------------

In Postman:

- Go to **Authorization**
- Select **Bearer Token**
- Paste the copied token

This must be done before using any `/todos` routes.

---------------------------------------------------------
6. Create a Todo
---------------------------------------------------------

Method: POST  
URL: http://127.0.0.1:5000/todos  
Body → raw → JSON:

{
  "task": "Buy milk",
  "status": "pending"
}

Expected Response: **201 Created**

{
    "id": "1",
    "owner": "richard",
    "status": "pending",
    "task": "Buy milk"
}

---------------------------------------------------------
7. Retrieve All Todos
---------------------------------------------------------

Method: GET  
URL: http://127.0.0.1:5000/todos  

Then 
- Go to **Authorization**
- Select **Bearer Token**
- Paste **Access Token Received From Previous Step 4**
- Click **Send**

Expected Response: **200 OK**

[
    {
        "id": "1",
        "owner": "richard",
        "status": "pending",
        "task": "Buy milk"
    }
]

---------------------------------------------------------
8. Update a Todo
---------------------------------------------------------

Method: Put  
URL: http://127.0.0.1:5000/todos/1  
Body → raw → JSON:

{
  "task": "Buy chicken",
  "status": "done"
}

Then 
- Go to **Authorization**
- Select **Bearer Token**
- Paste **Access Token Received From Previous Step 4**
- Click **Send**

Expected Response: **200 OK**

{
    "id": "1",
    "owner": "richard",
    "status": "done",
    "task": "Buy chicken"
}

---------------------------------------------------------
9. Delete a Todo
---------------------------------------------------------

Method: Delete  
URL: http://127.0.0.1:5000/todos/1  

Then 
- Go to **Authorization**
- Select **Bearer Token**
- Paste **Access Token Received From Previous Step 4**
- Click **Send**

Expected Response: **200 OK**

{
    "message": "Todo deleted successfully"
}

## Example API Call Log
- 127.0.0.1 - - [05/Dec/2025 00:24:29] "POST /register HTTP/1.1" 201 -
- 127.0.0.1 - - [05/Dec/2025 00:24:53] "POST /login HTTP/1.1" 200 -
- 127.0.0.1 - - [05/Dec/2025 00:25:37] "POST /todos HTTP/1.1" 201 -
- 127.0.0.1 - - [05/Dec/2025 00:26:01] "GET /todos HTTP/1.1" 200 -
- 127.0.0.1 - - [05/Dec/2025 00:26:29] "PUT /todos/1 HTTP/1.1" 200 -
- 127.0.0.1 - - [05/Dec/2025 00:26:52] "DELETE /todos/1 HTTP/1.1" 200 -