from flask import jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def user_add(req):
    post_data = req.form if req.form else req.json

    fields = ["email", "password"]
    req_fields = ["email", "password"]

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        values[field] = field_data

        if field in req_fields and not values[field]:
            return jsonify(f'{field} is required'), 400

    new_user = Users.get_new_user()
    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf8')

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201


def users_get_all():
    users_query = db.session.query(Users).all()

    return jsonify(users_schema.dump(users_query)), 200


def user_get_by_id(user_id):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    return jsonify(user_schema.dump(user_query)), 200


@authenticate_return_auth
def user_update_by_id(req, user_id, auth_info):
    post_data = req.form if req.form else req.json
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_query.user_id == auth_info.user_id:
        populate_object(user_query, post_data)
        db.session.commit()

        return jsonify(user_schema.dump(user_query)), 201

    return jsonify("Unauthorized: Cannot edit other users than yourself")


@authenticate_return_auth
def user_delete_by_id(req, user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_query.user_id == auth_info.user_id:

        db.session.delete(user_query)
        db.session.commit()

        return jsonify(f"user with id {user_id} has been delete "), 200

    return jsonify("Unauthorized: Cannot edit other users than yourself")
