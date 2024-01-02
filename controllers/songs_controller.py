from flask import jsonify

from db import db
from models.songs import Songs, song_schema, songs_schema
from models.chords import Chords
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


@authenticate_return_auth
def song_add(req, auth_info):
    post_data = req.form if req.form else req.json

    new_song = Songs.get_new_song(auth_info.user_id)
    populate_object(new_song, post_data)

    db.session.add(new_song)
    db.session.commit()

    return jsonify(song_schema.dump(new_song)), 201


def songs_get_all():
    songs_query = db.session.query(Songs).all()

    return jsonify(songs_schema.dump(songs_query)), 200


def song_get_by_id(song_id):
    song_query = db.session.query(Songs).filter(Songs.song_id == song_id).first()

    return jsonify(song_schema.dump(song_query)), 200


@authenticate_return_auth
def song_update_by_id(req, song_id, auth_info):
    post_data = req.form if req.form else req.json
    song_query = db.session.query(Songs).filter(Songs.song_id == song_id).first()

    if song_query.creator_id == auth_info.user_id:
        populate_object(song_query, post_data)
        db.session.commit()

        return jsonify(song_schema.dump(song_query)), 201

    return jsonify("Unauthorized: Cannot edit Songs created by other users")


@authenticate_return_auth
def song_delete_by_id(req, song_id, auth_info):
    song_query = db.session.query(Songs).filter(Songs.song_id == song_id).first()

    if song_query.creator_id == auth_info.user_id:
        db.session.delete(song_query)
        db.session.commit()

        return jsonify(f"song with id {song_id} has been delete "), 200

    return jsonify("Unauthorized: Cannot delete Songs created by other users")


@authenticate_return_auth
def song_add_chord(req, auth_info):
    post_data = req.form if req.form else req.json
    song_id = post_data.get("song_id")
    chord_id = post_data.get("chord_id")

    song_query = db.session.query(Songs).filter(Songs.song_id == song_id).first()
    chord_query = db.session.query(Chords).filter(Chords.chord_id == chord_id).first()

    if song_query.creator_id == auth_info.user_id:
        if song_query and chord_query:
            song_query.chords.append(chord_query)
            db.session.commit()

            return jsonify(song_schema.dump(song_query)), 201

        else:
            return jsonify("ERROR: song_id and/or chord_id not found")

    return jsonify("Unauthorized: Cannot edit Songs created by other users")
