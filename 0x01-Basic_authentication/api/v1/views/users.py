#!/usr/bin/env python3
"""Users views module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    """
    userj = None
    error_msg = None
    try:
        userj = request.get_json()
    except Exception as e:
        userj = None
    if userj is None:
        error_msg = "Wrong format"
    if error_msg is None and userj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and userj.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = userj.get("email")
            user.password = userj.get("password")
            user.first_name = userj.get("first_name")
            user.last_name = userj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    userj = None
    try:
        userj = request.get_json()
    except Exception as e:
        userj = None
    if userj is None:
        return jsonify({'error': "Wrong format"}), 400
    if userj.get('first_name') is not None:
        user.first_name = userj.get('first_name')
    if userj.get('last_name') is not None:
        user.last_name = userj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200