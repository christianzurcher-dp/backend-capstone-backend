from flask import request, Blueprint

import controllers


time_signatures = Blueprint('time_signatures', __name__)


@time_signatures.route("/time_signature", methods=["POST"])
def time_signature_add():
    return controllers.time_signature_add(request)


@time_signatures.route("/time_signatures", methods=["GET"])
def time_signatures_get_all():
    return controllers.time_signatures_get_all()


@time_signatures.route("/time_signature/<time_signature_id>", methods=["GET"])
def time_signature_get_by_id(time_signature_id):
    return controllers.time_signature_get_by_id(time_signature_id)


@time_signatures.route("/time_signature/<time_signature_id>", methods=["PUT"])
def time_signature_update_by_id(time_signature_id):
    return controllers.time_signature_update_by_id(request, time_signature_id)


@time_signatures.route("/time_signature/<time_signature_id>", methods=["DELETE"])
def time_signature_delete_by_id(time_signature_id):
    return controllers.time_signature_delete_by_id(request, time_signature_id)
