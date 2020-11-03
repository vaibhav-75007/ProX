'''
This file is part of ProX.

ProX is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ProX is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ProX.  If not, see <https://www.gnu.org/licenses/>
'''

from flask import request
from flask_api import FlaskAPI, status, exceptions
from Server import Server
from Database import DB

IP = '0.0.0.0'
PORT = 54321
DB_PATH = "db.json"

server = Server(DB_PATH)
api = FlaskAPI("ProX")


def check_db_loaded():
    """
    Check if DB is loaded into memory (i.e. idling). If not, load DB into memory
    """
    if not server.DBLoaded:
        server.LoadDB()


def user_validation(user_id, pin):
    """
    Check if user with user_id exists. If yes, check if personal pin matches
    """
    # Try querying user with ID user_id
    try:
        user = server.DB.QueryUser(user_id)
    except KeyError as ke:
        raise exceptions.NotFound(str(ke))
    
    # Comparing provided pin with the pin stored in the database
    if pin != user["pin"]:
        raise exceptions.AuthenticationFailed("Authentication Failed (User ID and PIN not matched)")


@api.route("/", methods=['GET'])
def ping_server():
    """
    Ping the server
    """
    return "ProX server is working", status.HTTP_200_OK


@api.route("/<int:user_id>/<int:pin>/everyone/", methods=['GET'])
def get_everyone(user_id, pin):
    """
    Get public data from every user for the leaderboard, EXCEPT the user that making the request
    """
    
    check_db_loaded()
    user_validation(user_id, pin)
    
    users = list()
    for user in server.DB.Users:
        if user["id"] == user_id:
            continue # Skip the user that is requesting
        adding = user.copy()
        del adding["id"], adding["pin"], adding["email"] # Remove sensitive data
        users.append(adding)
    return users, status.HTTP_200_OK


@api.route("/<int:user_id>/<int:pin>/", methods=['GET', 'PUT', 'DELETE'])
def user_request(user_id, pin):
    """
    Handle GET, PUT and DELETE requests from users.
    GET: query a user's data
    PUT: update a user's data
    DELETE: delete a user from the database
    """

    check_db_loaded()
    user_validation(user_id, pin)

    if request.method == 'GET':
        return server.DB.QueryUser(user_id), status.HTTP_200_OK

    elif request.method == 'PUT':
        data = request.get_json(force = True, silent = True)
        try:
            # Perform type checking on data received
            DB.TypeCheckExistingUser(data)
            # Update the database based on data received
            user = server.DB.ModUser(
                user_id = user_id,
                name = data["name"],
                email = data["email"],
                pin = data["pin"],
                productivity_score = data["productivity_score"],
                task_completion_rate = data["task_completion_rate"],
                missed_deadline = data["missed_deadline"],
                weekly_productivity_score = data["weekly_productivity_score"],
                weekly_task_completion_rate = data["weekly_task_completion_rate"],
                weekly_deadlines_missed = data["weekly_deadlines_missed"],
                tasks = data["tasks"],
                flashcards = data["flashcards"],
                curriculums = data["curriculums"]
            )
            return user, status.HTTP_200_OK
        except Exception as e:
            raise exceptions.ParseError(str(e))

    elif request.method == 'DELETE':
        server.DB.DelUser(user_id)
        return "OK", status.HTTP_200_OK


@api.route("/new/", methods=['POST'])
def create_user():
    """
    Handle POST method to create a new user.
    Respond with this new user object
    """

    check_db_loaded()

    data = request.get_json(force = True, silent = True)
    try:
        # Perform type checking on data received
        DB.TypeCheckNewUser(data)
        # Create new user based on data received
        user = server.DB.AddUser(
            name = data["name"],
            email = data["email"],
            pin = data["pin"]
        )
        return user, status.HTTP_200_OK
    except Exception as e:
        raise exceptions.ParseError(str(e))


@api.route("/recover/", methods=['GET'])
def recover():
    """
    Recover a user object from the email address and PIN number
    """
    
    check_db_loaded()
        
    data = request.get_json(force = True, silent = True)
    
    try:
        email = data["email"]
        pin = data["pin"]
    except KeyError as ke:
        raise exceptions.ParseError(str(ke))

    user = server.DB.FindUserByEmail(email)
    if not user:
        raise exceptions.NotFound(f"User with email {email} not found")
    elif pin != user["pin"]:
        raise exceptions.AuthenticationFailed("Authentication Failed (Email and PIN not matched)")
    return user, status.HTTP_200_OK


if __name__ == "__main__":
    api.run(host=IP, port=PORT)
