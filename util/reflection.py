from flask import jsonify


def populate_object(Obj, data_dictionary):
    fields = data_dictionary.keys()

    for field in fields:
        try:
            getattr(Obj, field)
            setattr(Obj, field, data_dictionary[field])

        except AttributeError:
            return jsonify({'ERROR': f"Record has no attribute: {field}"}), 400
