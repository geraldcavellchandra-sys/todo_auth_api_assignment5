from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Change if needed

jwt = JWTManager(app)

USERS_FILE = "users.json"
TODOS_FILE = "todos.json"


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        try:
            return json.load(f)
        except:
            return {}


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


users = load_json(USERS_FILE)
todos = load_json(TODOS_FILE)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"message": "Username and password required"}, 400

    if username in users:
        return {"message": "User already exists"}, 400

    users[username] = {
        "password": generate_password_hash(password)
    }
    save_json(USERS_FILE, users)

    return {"message": "User registered successfully"}, 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)

    if not user or not check_password_hash(user["password"], password):
        return {"message": "Invalid username or password"}, 401

    token = create_access_token(identity=username)
    return {"access_token": token}, 200


@app.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    current_user = get_jwt_identity()
    user_todos = [t for t in todos.values() if t["owner"] == current_user]
    return jsonify(user_todos), 200


@app.route('/todos', methods=['POST'])
@jwt_required()
def add_todo():
    current_user = get_jwt_identity()
    data = request.get_json()

    new_id = str(len(todos) + 1)

    todos[new_id] = {
        "id": new_id,
        "task": data.get("task"),
        "status": data.get("status", "pending"),
        "owner": current_user
    }

    save_json(TODOS_FILE, todos)
    return jsonify(todos[new_id]), 201


@app.route('/todos/<string:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    current_user = get_jwt_identity()

    if todo_id not in todos:
        return {"message": "Todo not found"}, 404

    todo = todos[todo_id]

    if todo["owner"] != current_user:
        return {"message": "Unauthorized"}, 403

    update_data = request.get_json()
    todo.update(update_data)

    save_json(TODOS_FILE, todos)
    return jsonify(todo), 200


@app.route('/todos/<string:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    current_user = get_jwt_identity()

    if todo_id not in todos:
        return {"message": "Todo not found"}, 404

    if todos[todo_id]["owner"] != current_user:
        return {"message": "Unauthorized"}, 403

    del todos[todo_id]
    save_json(TODOS_FILE, todos)

    return {"message": "Todo deleted successfully"}, 200


if __name__ == '__main__':
    app.run(debug=True)
