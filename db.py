import datetime

db = {
    'users': {
        1: {
            'name': "John Doe",
            'email': "johndoe@company.com",
            'role_id': None,
            'current_event_id': 1,  # Event ID for "Tech Conference 2024"
            'last_activity': "2024-12-05 14:30",
            'status': "Active"
        },
        2: {
            'name': "Jane Smith",
            'email': "janesmith@company.com",
            'role_id': 2,
            'current_event_id': 2,  # Event ID for "AI Summit 2024"
            'last_activity': "2024-11-21 09:00",
            'status': "Active"
        },
        3: {
            'name': "Mark Taylor",
            'email': "marktaylor@company.com",
            'role_id': 3,
            'current_event_id': None,  # No active event for this user (Inactive status)
            'last_activity': "2024-11-05 12:45",
            'status': "Inactive"
        },
        4: {
            'name': "Alice Brown",
            'email': "alicebrown@company.com",
            'role_id': 2,
            'current_event_id': 4,  # Event ID for "Startup Meetup"
            'last_activity': "2024-11-15 16:00",
            'status': "Active"
        },
        5: {
            'name': "Robert Clark",
            'email': "robertclark@company.com",
            'role_id': 3,
            'current_event_id': None,  # No active event for this user (Inactive status)
            'last_activity': "2024-10-29 10:15",
            'status': "Inactive"
        },
        6: {
            'name': "Emily Davis",
            'email': "emilydavis@company.com",
            'role_id': 1,
            'current_event_id': 1,  # Event ID for "Tech Conference 2024"
            'last_activity': "2024-12-03 18:00",
            'status': "Active"
        },
        7: {
            'name': "Chris Miller",
            'email': "chrismiller@company.com",
            'role_id': 3,
            'current_event_id': 2,  # Event ID for "AI Summit 2024"
            'last_activity': "2024-11-10 09:30",
            'status': "Active"
        },
        8: {
            'name': "Jessica Lee",
            'email': "jessicalee@company.com",
            'role_id': 2,
            'current_event_id': 3,  # Event ID for "Product Launch"
            'last_activity': "2024-11-22 11:00",
            'status': "Active"
        },
        9: {  # Added new user for coordinator role in event 4
            'name': "Samuel Green",
            'email': "samuelgreen@company.com",
            'role_id': 3,
            'current_event_id': 4,  # Event ID for "Startup Meetup"
            'last_activity': "2024-11-10 14:30",
            'status': "Active"
        },
        10: {  # Added new user for coordinator role in event 5
            'name': "Natalie White",
            'email': "nataliewhite@company.com",
            'role_id': 3,
            'current_event_id': 5,  # Event ID for "AI Expo 2024"
            'last_activity': "2024-11-10 14:30",
            'status': "Active"
        },
        11: {  # Added new user for coordinator role in event 5
            'name': "David Johnson",
            'email': "davidjohnson@company.com",
            'role_id': 3,
            'current_event_id': 5,  # Event ID for "AI Expo 2024"
            'last_activity': "2024-11-10 14:30",
            'status': "Active"
        }
    },

    'events': {
        1: {
            'event_name': "Tech Conference 2024",
            'description': "A major conference showcasing the latest advancements in technology.",
            'location': "San Francisco, CA",
            'start_datetime': "2024-12-15 09:00",
            'end_datetime': "2024-12-15 17:00",
            'event_admin': 1,  # Admin ID
            'event_coordinators': [2, 4, 5]  # List of Event Coordinator IDs
        },
        2: {
            'event_name': "AI Summit 2024",
            'description': "An event bringing together experts to discuss AI technologies.",
            'location': "New York, NY",
            'start_datetime': "2024-12-20 09:00",
            'end_datetime': "2024-12-20 18:00",
            'event_admin': 2,  # Admin ID
            'event_coordinators': [3, 7]  # List of Event Coordinator IDs
        },
        3: {
            'event_name': "Product Launch",
            'description': "The launch event for the company's latest product.",
            'location': "Los Angeles, CA",
            'start_datetime': "2024-12-10 10:00",
            'end_datetime': "2024-12-10 15:00",
            'event_admin': 3,  # Admin ID
            'event_coordinators': [6, 8]  # List of Event Coordinator IDs
        },
        4: {
            'event_name': "Startup Meetup",
            'description': "A networking event for startup founders and investors.",
            'location': "Chicago, IL",
            'start_datetime': "2024-12-05 14:00",
            'end_datetime': "2024-12-05 19:00",
            'event_admin': 4,  # Admin ID
            'event_coordinators': [5, 9]  # List of Event Coordinator IDs
        },
        5: {
            'event_name': "AI Expo 2024",
            'description': "An expo showcasing the latest in artificial intelligence and machine learning.",
            'location': "Boston, MA",
            'start_datetime': "2024-12-18 10:00",
            'end_datetime': "2024-12-18 16:00",
            'event_admin': 5,  # Admin ID
            'event_coordinators': [10, 11]  # List of Event Coordinator IDs
        }
    },

    'roles': {
    1: {'role_name': "admin", 'permissions': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'description': 'Has full access to manage all users, roles, permissions, and events.'},
    2: {'role_name': "event-admin", 'permissions': [5, 6, 7, 8, 17], 'description': 'Can manage event details, participants, and resources, but cannot manage user roles.'},
    3: {'role_name': "event-coordinator", 'permissions': [1, 2, 3, 4, 5, 6, 7, 8, 17], 'description': 'Can manage events, view and modify participants, and handle event logistics.'},
    4: {"role_name": "guest", 'permissions': [6, 17], 'description': 'Has limited access, can only view event details and resources.'}
},

    'permissions' : {
    1: {'permission_name': "create-user", 'context': "user", 'description': "Allows the creation of a new user."},
    2: {'permission_name': "read-user", 'context': "user", 'description': "Allows viewing user details."},
    3: {'permission_name': "update-user", 'context': "user", 'description': "Allows updating user information."},
    4: {'permission_name': "delete-user", 'context': "user", 'description': "Allows deleting a user."},

    5: {'permission_name': "create-event", 'context': "event", 'description': "Allows the creation of a new event."},
    6: {'permission_name': "read-event", 'context': "event", 'description': "Allows viewing event details."},
    7: {'permission_name': "update-event", 'context': "event", 'description': "Allows updating event information."},
    8: {'permission_name': "delete-event", 'context': "event", 'description': "Allows deleting an event."},

    9: {'permission_name': "create-role", 'context': "role", 'description': "Allows the creation of a new role."},
    10: {'permission_name': "read-role", 'context': "role", 'description': "Allows viewing role details."},
    11: {'permission_name': "update-role", 'context': "role", 'description': "Allows updating role information."},
    12: {'permission_name': "delete-role", 'context': "role", 'description': "Allows deleting a role."},

    13: {'permission_name': "create-permission", 'context': "rules",
         'description': "Allows creating a new permission."},
    14: {'permission_name': "read-permission", 'context': "rules",
         'description': "Allows viewing permission details."},
    15: {'permission_name': "update-permission", 'context': "rules",
         'description': "Allows updating permission information."},
    16: {'permission_name': "delete-permission", 'context': "rules",
         'description': "Allows deleting a permission."},

    # common permissions
    17: {'permission_name': "view-dashboard", 'context': "dashboard",
         'description': "Allows viewing the dashboard."},
    18: {'permission_name': "view-settings", 'context': "settings",
         'description': "Allows viewing the settings."},
    19: {'permission_name': "view-audit-logs", 'context': 'audit-logs',
         'description': 'Allows viewing the logs'}
   }
}


class Base:
    def __init__(self, db):
        self.db = db

    def fetch_related_data(self, item, relation_key, relation_db, relation_field, is_list=False):
        """
        Fetches related data for a given item.
        :param item: The item (user, role, event) dictionary.
        :param relation_key: The key in the item that links to the related entity (e.g., role_id, event_id).
        :param relation_db: The related database to fetch data from (e.g., self.db['roles'], self.db['events']).
        :param relation_field: The field from the related entity to retrieve (e.g., 'role_name', 'event_name').
        :param is_list: Whether the relation_key is a list of IDs (default is False).
        :return: The related data field or None. If is_list is True, returns a list of related data.
        """
        if is_list:
            # If it's a list of IDs, map over them to get the related data
            return [relation_db.get(related_id).get(relation_field) if relation_db.get(related_id) else None
                    for related_id in item.get(relation_key, [])]
        else:
            related_id = item.get(relation_key)
            if related_id:
                related_entity = relation_db.get(related_id)
                return related_entity.get(relation_field) if related_entity else None
            return None


class User(Base):
    def __init__(self, db):
        super().__init__(db)  # Initialize the Base class with db

    def create(self, user_data):
        new_id = max(self.db['users'].keys()) + 1 if self.db['users'] else 1
        self.db['users'][new_id] = user_data
        return new_id

    def read(self, user_id):
        return self.db['users'].get(user_id)

    def update(self, user_id, updated_data):
        if user_id in self.db['users']:
            self.db['users'][user_id].update(updated_data)
            return True
        return False

    def delete(self, user_id):
        if user_id in self.db['users']:
            del self.db['users'][user_id]
            return True
        return False

    def get_all(self):
        return self.db['users']

    def get_all_as_list(self):
        users = []
        for key, user in self.db['users'].items():
            user['id'] = key
            user['role'] = self.fetch_related_data(user, 'role_id', self.db['roles'], 'role_name')
            user['current_event'] = self.fetch_related_data(user, 'current_event_id', self.db['events'], 'event_name')
            users.append(user)
        return users

class Role(Base):
    def __init__(self, db):
        super().__init__(db)  # Initialize the Base class with db

    def create(self, role_data):
        new_id = max(self.db['roles'].keys()) + 1 if self.db['roles'] else 1
        self.db['roles'][new_id] = role_data
        print(self.db['roles'])
        return new_id

    def read(self, role_id):
        print("role read :", role_id, self.db['roles'].get(role_id))
        return self.db['roles'].get(role_id)

    def update(self, role_id, updated_data):
        if role_id in self.db['roles']:
            self.db['roles'][role_id].update(updated_data)
            return True
        return False

    def delete(self, role_id):
        if role_id in self.db['roles']:
            del self.db['roles'][role_id]
            return True
        return False

    def get_all(self):
        return self.db['roles']

    def get_all_as_list(self):
        roles = [{**role, "id" : key} for key, role in self.db['roles'].items()]
        return roles

    def get_role_permissions(self, role_id):
        role = self.db['roles'].get(role_id, None)

        if role:
            permissions = self.fetch_related_data(role, "permissions", self.db['permissions'], "permission_name", is_list=True)
            return permissions
        return None


class Permission(Base):
    def __init__(self, db):
        super().__init__(db)  # Initialize the Base class with db

    def create(self, permission_data):
        new_id = max(self.db['permissions'].keys()) + 1 if self.db['permissions'] else 1
        self.db['permissions'][new_id] = permission_data
        return new_id

    def read(self, permission_id):
        return self.db['permissions'].get(permission_id)

    def update(self, permission_id, updated_data):
        print(permission_id, updated_data)
        if permission_id in self.db['permissions']:
            self.db['permissions'][permission_id].update(updated_data)
            return True
        return False

    def delete(self, permission_id):
        if permission_id in self.db['permissions']:
            del self.db['permissions'][permission_id]
            return True
        return False

    def get_all(self):
        return self.db['permissions']

    def get_all_as_list(self):
        permissions = [{**perm, "id": key} for key, perm in self.db['permissions'].items()]
        return permissions


class Event(Base):
    def __init__(self, db):
        super().__init__(db)  # Initialize the Base class with db

    def create(self, event_data):
        new_id = max(self.db['events'].keys()) + 1 if self.db['events'] else 1
        self.db['events'][new_id] = event_data

        return new_id

    def read(self, event_id):
        return self.db['events'].get(event_id)

    def update(self, event_id, updated_data):
        if event_id in self.db['events']:
            self.db['events'][event_id].update(updated_data)
            return True
        return False

    def delete(self, event_id):
        if event_id in self.db['events']:
            del self.db['events'][event_id]
            return True
        return False

    def get_all(self):
        return self.db['events']

    def get_all_as_list(self):
        events = [{**event , "id": key} for key, event in self.db['events'].items()]
        return events


    def get_event_by_user(self, user_id):
        events = []
        for event_id, event in self.db['events'].items():
            if user_id in event['event_coordinators'] or event['event_admin'] == user_id:
                events.append(event)
        return events

