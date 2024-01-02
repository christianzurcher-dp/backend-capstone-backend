from flask import jsonify

from db import db
from models.chords import Chords, chord_schema, chords_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def chord_add(req):
    post_data = req.form if req.form else req.json

    new_chord = Chords.get_new_chord()
    populate_object(new_chord, post_data)

    db.session.add(new_chord)
    db.session.commit()

    return jsonify(chord_schema.dump(new_chord)), 201


def chords_get_all():
    chords_query = db.session.query(Chords).all()

    return jsonify(chords_schema.dump(chords_query)), 200


def chord_get_by_id(chord_id):
    chord_query = db.session.query(Chords).filter(Chords.chord_id == chord_id).first()

    return jsonify(chord_schema.dump(chord_query)), 200


@authenticate_return_auth
def chord_update_by_id(req, chord_id, auth_info):
    post_data = req.form if req.form else req.json
    chord_query = db.session.query(Chords).filter(Chords.chord_id == chord_id).first()

    if chord_query.creator_id == auth_info.user_id:
        populate_object(chord_query, post_data)
        db.session.commit()

        return jsonify(chord_schema.dump(chord_query)), 201

    return jsonify("Unauthorized: Cannot edit Chords created by other users")


def chord_delete_by_id(req, chord_id, auth_info):
    chord_query = db.session.query(Chords).filter(Chords.chord_id == chord_id).first()

    if chord_query.creator_id == auth_info.user_id:
        db.session.delete(chord_query)
        db.session.commit()

        return jsonify(f"chord with id {chord_id} has been delete "), 200

    return jsonify("Unauthorized: Cannot delete Chords created by other users")
