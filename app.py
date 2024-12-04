from flask import Flask, jsonify, request
import datetime
import logging
from typing import Optional, List
from pydantic import BaseModel, ValidationError
from db import db, User, Role, Permission, Event
from flask_cors import CORS
import copy
import os

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the helper classes
user_helper = User(db)
role_helper = Role(db)
permission_helper = Permission(db)
event_helper = Event(db)

def rebuild_roles_map():
    global rolesMap
    roles = role_helper.get_all_as_list()
    rolesMap = {role['id']: role['role_name'] for role in roles}
    logger.info("rolesMap updated: %s", rolesMap)

rebuild_roles_map()

# Pydantic models for data validation
class UserCreateModel(BaseModel):
    name: str
    email: str
    role_id: Optional[int] = None
    current_event: Optional[str] = None
    last_activity: Optional[str] = datetime.datetime.now()
    status: Optional[str] = 'Active'


class RoleCreateModel(BaseModel):
    role_name: str
    description: str
    permissions: Optional[List[int]] = []


class PermissionCreateModel(BaseModel):
    permission_name: str
    description: str
    context: str


class EventCreateModel(BaseModel):
    event_name: str
    description: str
    location: str
    start_datetime: str
    end_datetime: str
    event_admin: Optional[int] = None
    event_coordinators: Optional[list[int]] = []


# ---------------- Mock Login ---------------------#
@app.route('/login', methods=['POST'])
def mock_login():
    try:
        # Get the role from request body
        data = request.get_json()
        role_id = int(data.get('role', 1))

        logger.info(f"Received role_id: {role_id}")

        # Fetch role details
        curr_role = copy.deepcopy(role_helper.read(role_id))
        logger.info(f"Fetched role: {curr_role}")

        permissions = []
        for perm_id in curr_role['permissions']:
            perm_obj = copy.deepcopy(permission_helper.read(perm_id))
            if perm_obj:
                permissions.append(perm_obj)
        curr_role['permissions'] = permissions

        user = {
            "id": 1,
            "name": "MockUser",
            "email": "mockuser@example.com"
        }

        response = {
            "user": user,
            "role": curr_role,
        }

        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        return jsonify({"message": "An error occurred during login"}), 500


# ---------------- Routes for Users ----------------
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = user_helper.get_all_as_list()
        return jsonify(users)
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return jsonify({"message": "Failed to fetch users"}), 500


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = user_helper.read(user_id)
        if user:
            return jsonify(user)
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {str(e)}")
        return jsonify({"message": "An error occurred"}), 500


@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = request.get_json()
        logger.info(f"Received user data: {user_data}")
        # Validate with Pydantic
        user_model = UserCreateModel(**user_data)
        user_id = user_helper.create(user_model.dict())
        user = user_helper.read(user_id)
        user['id'] = user_id
        logger.info(f"User created: {user}")
        return jsonify({"message": "User created", "user": user}), 201
    except ValidationError as e:
        logger.error(f"Validation error: {e.errors()}")
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({"message": "An error occurred"}), 500


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        updated_data = request.get_json()
        if user_helper.update(user_id, updated_data):
            user = user_helper.read(user_id)
            user['role'] = rolesMap.get(int(user['role_id']), 'Unknown')
            logger.info(f"User updated: {user}")
            return jsonify(user)
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        return jsonify({"message": "An error occurred"}), 500


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        if user_helper.delete(user_id):
            return jsonify({"message": "User deleted"})
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({"message": "An error occurred"}), 500


# ---------------- Routes for Roles ----------------
@app.route('/roles', methods=['GET'])
def get_roles():
    try:
        roles = role_helper.get_all_as_list()
        return jsonify(roles)
    except Exception as e:
        logger.error(f"Error fetching roles: {str(e)}")
        return jsonify({"message": "Failed to fetch roles"}), 500


@app.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    try:
        role = role_helper.read(role_id)
        if role:
            return jsonify(role)
        return jsonify({"message": "Role not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching role {role_id}: {str(e)}")
        return jsonify({"message": "An error occurred"}), 500


@app.route('/roles', methods=['POST'])
def create_role():
    try:
        role_data = request.get_json()
        role_model = RoleCreateModel(**role_data)
        role_id = role_helper.create(role_model.dict())
        rebuild_roles_map()
        logger.info(f"Role created: {role_id}")
        return jsonify({"message": "Role created", "role_id": role_id}), 201
    except ValidationError as e:
        logger.error(f"Validation error: {e.errors()}")
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        logger.error(f"Error creating role: {str(e)}")
        return jsonify({"message": "An error occurred"}), 500


# ---------------- Routes for Permissions ----------------
@app.route('/permissions', methods=['GET'])
def get_permissions():
    try:
        permissions = permission_helper.get_all_as_list()
        return jsonify(permissions)
    except Exception as e:
        logger.error(f"Error fetching permissions: {str(e)}")
        return jsonify({"message": "Failed to fetch permissions"}), 500


# ---------------- Routes for Events ----------------
@app.route('/events', methods=['GET'])
def get_events():
    try:
        events = event_helper.get_all_as_list()
        return jsonify(events)
    except Exception as e:
        logger.error(f"Error fetching events: {str(e)}")
        return jsonify({"message": "Failed to fetch events"}), 500


if __name__ == "__main__":
    app.run(debug=True)
