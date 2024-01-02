import routes


def register_blueprints(app):
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.time_signatures)
    app.register_blueprint(routes.chords)
    app.register_blueprint(routes.songs)
    app.register_blueprint(routes.auth)
