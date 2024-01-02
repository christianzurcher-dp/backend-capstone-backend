from flask import jsonify

from db import db
from models.time_signatures import TimeSignatures, time_signature_schema, time_signatures_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


@authenticate_return_auth
def time_signature_add(req, auth_info):
    post_data = req.form if req.form else req.json

    new_time_signature = TimeSignatures.get_new_time_signature(auth_info.user_id)
    populate_object(new_time_signature, post_data)

    db.session.add(new_time_signature)
    db.session.commit()

    return jsonify(time_signature_schema.dump(new_time_signature)), 201


def time_signatures_get_all():
    time_signatures_query = db.session.query(TimeSignatures).all()

    return jsonify(time_signatures_schema.dump(time_signatures_query)), 200


def time_signature_get_by_id(time_signature_id):
    time_signature_query = db.session.query(TimeSignatures).filter(TimeSignatures.time_signature_id == time_signature_id).first()

    return jsonify(time_signature_schema.dump(time_signature_query)), 200


@authenticate_return_auth
def time_signature_update_by_id(req, time_signature_id, auth_info):
    post_data = req.form if req.form else req.json
    time_signature_query = db.session.query(TimeSignatures).filter(TimeSignatures.time_signature_id == time_signature_id).first()

    if time_signature_query.creator_id == auth_info.user_id:
        populate_object(time_signature_query, post_data)
        db.session.commit()

        return jsonify(time_signature_schema.dump(time_signature_query)), 201

    return jsonify("Unauthorized: Cannot edit Time Signatures created by other users")


@authenticate_return_auth
def time_signature_delete_by_id(req, time_signature_id, auth_info):
    time_signature_query = db.session.query(TimeSignatures).filter(TimeSignatures.time_signature_id == time_signature_id).first()

    if time_signature_query.creator_id == auth_info.user_id:
        db.session.delete(time_signature_query)
        db.session.commit()

        return jsonify(f"time_signature with id {time_signature_id} has been delete "), 200

    return jsonify("Unauthorized: Cannot delete Time Signatures created by other users")
