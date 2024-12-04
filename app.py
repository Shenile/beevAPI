from flask import Flask, jsonify, request
import datetime
from typing import Optional, List
from pydantic import BaseModel, ValidationError
from db import db, User, Role, Permission, Event
from flask_cors import CORS
import copy

app = Flask(__name__)
CORS(app)
# Initialize the helper classes
user_helper = User(db)
role_helper = Role(db)
permission_helper = Permission(db)
event_helper = Event(db)

def rebuild_roles_map():
    global rolesMap
    roles = role_helper.get_all_as_list()
    rolesMap = {role['id']: role['role_name'] for role in roles}
    print("rolesMap updated:", rolesMap)

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

#----------------- Mock Login ---------------------#
@app.route('/login', methods=['POST'])
def mock_login():
    # Get the role from request body
    data = request.get_json()
    role_id = int(data.get('role', 1))

    print(f"Received role_id: {role_id}")

    # Fetch role details
    curr_role = copy.deepcopy(role_helper.read(role_id))
    print(f"Fetched role: {curr_role}")

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


# ---------------- Routes for Users ----------------
@app.route('/users', methods=['GET'])
def get_users():
    users = user_helper.get_all_as_list()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = user_helper.read(user_id)
        if user:
            return jsonify(user)
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = request.get_json()
        print(user_data)
        # Validate with Pydantic
        user_model = UserCreateModel(**user_data)
        user_id = user_helper.create(user_model.dict())
        user = user_helper.read(user_id)
        user['id'] = user_id
        print(user)
        return jsonify({"message": "User created", "user": user}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        updated_data = request.get_json()
        if user_helper.update(user_id, updated_data):
            user = user_helper.read(user_id)
            user['role'] = rolesMap[int(user['role_id'])]
            print('sending response : ', user)
            return jsonify(user)
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        if user_helper.delete(user_id):
            return jsonify({"message": "User deleted"})
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# ---------------- Routes for Roles ----------------
@app.route('/roles', methods=['GET'])
def get_roles():
    try:
        roles = role_helper.get_all_as_list()
        return jsonify(roles)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    try:
        role = role_helper.read(role_id)
        if role:
            return jsonify(role)
        return jsonify({"message": "Role not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/roles', methods=['POST'])
def create_role():
    try:
        role_data = request.get_json()
        role_model = RoleCreateModel(**role_data)  # Validate with Pydantic
        print(role_model)
        role_id = role_helper.create(role_model.dict())
        rebuild_roles_map()
        print(rolesMap[role_id])
        return jsonify({"message": "Role created", "role_id": role_id}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    try:
        updated_data = request.get_json()
        if role_helper.update(role_id, updated_data):
            return jsonify({"message": "Role updated"})

        return jsonify({"message": "Role not found"}), 404
    except Exception as e:
        print(f'ERROR : {e}')
        return jsonify({"message": str(e)}), 500

@app.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    try:
        if role_helper.delete(role_id):
            return jsonify({"message": "Role deleted"})
        return jsonify({"message": "Role not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# ---------------- Routes for Permissions ----------------
@app.route('/permissions', methods=['GET'])
def get_permissions():
    try:
        permissions = permission_helper.get_all_as_list()
        return jsonify(permissions)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/permissions/<int:permission_id>', methods=['GET'])
def get_permission(permission_id):
    try:
        permission = permission_helper.read(permission_id)
        if permission:
            return jsonify(permission)
        return jsonify({"message": "Permission not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/permissions', methods=['POST'])
def create_permission():
    try:
        permission_data = request.get_json()
        permission_model = PermissionCreateModel(**permission_data)  # Validate with Pydantic
        permission_id = permission_helper.create(permission_model.dict())
        return jsonify({"message": "Permission created", "permission_id": permission_id}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/permissions/<int:permission_id>', methods=['PUT'])
def update_permission(permission_id):
    try:
        updated_data = request.get_json()
        if permission_helper.update(permission_id, updated_data):
            return jsonify({"message": "Permission updated"})

        return jsonify({"message": "Permission not found"}), 404
    except Exception as e:
        print(f'ERROR : {e}')
        return jsonify({"message": str(e)}), 500

@app.route('/permissions/<int:permission_id>', methods=['DELETE'])
def delete_permission(permission_id):
    try:
        print(permission_id)
        print(permission_helper.read(permission_id))
        if permission_helper.delete(permission_id):
            return jsonify({"message": "Permission deleted"})
        return jsonify({"message": "Permission not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# ---------------- Routes for Events ----------------
@app.route('/events', methods=['GET'])
def get_events():
    try:
        events = event_helper.get_all_as_list()
        return jsonify(events)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    try:
        event = event_helper.read(event_id)
        if event:
            return jsonify(event)
        return jsonify({"message": "Event not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/events', methods=['POST'])
def create_event():
    try:
        event_data = request.get_json()
        event_model = EventCreateModel(**event_data)  # Validate with Pydantic
        event_id = event_helper.create(event_model.dict())
        return jsonify({"message": "Event created", "event_id": event_id}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        updated_data = request.get_json()
        if event_helper.update(event_id, updated_data):
            return jsonify({"message": "Event updated"})
        return jsonify({"message": "Event not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        if event_helper.delete(event_id):
            return jsonify({"message": "Event deleted"})
        return jsonify({"message": "Event not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
