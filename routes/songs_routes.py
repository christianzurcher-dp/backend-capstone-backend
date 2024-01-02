from flask import request, Blueprint

import controllers


songs = Blueprint('songs', __name__)


@songs.route("/song", methods=["POST"])
def song_add():
    return controllers.song_add(request)


@songs.route("/songs", methods=["GET"])
def songs_get_all():
    return controllers.songs_get_all()


@songs.route("/song/<song_id>", methods=["GET"])
def song_get_by_id(song_id):
    return controllers.song_get_by_id(song_id)


@songs.route("/song/<song_id>", methods=["PUT"])
def song_update_by_id(song_id):
    return controllers.song_update_by_id(request, song_id)


@songs.route("/song/<song_id>", methods=["DELETE"])
def song_delete_by_id(song_id):
    return controllers.song_delete_by_id(request, song_id)


@songs.route("/song/chord-add", methods=["POST"])
def song_add_chord():
    return controllers.song_add_chord(request)
