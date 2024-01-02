from flask import request, Blueprint

import controllers


chords = Blueprint('chords', __name__)


@chords.route("/chord", methods=["POST"])
def chord_add():
    return controllers.chord_add(request)


@chords.route("/chords", methods=["GET"])
def chords_get_all():
    return controllers.chords_get_all()


@chords.route("/chord/<chord_id>", methods=["GET"])
def chord_get_by_id(chord_id):
    return controllers.chord_get_by_id(chord_id)


@chords.route("/chord/<chord_id>", methods=["PUT"])
def chord_update_by_id(chord_id):
    return controllers.chord_update_by_id(request, chord_id)


@chords.route("/chord/<chord_id>", methods=["DELETE"])
def chord_delete_by_id(chord_id):
    return controllers.chord_delete_by_id(request, chord_id)
