import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.chords_songs_xref import chords_songs_xref


class Chords(db.Model):
    __tablename__ = "Chords"

    chord_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    chord_name = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String(), nullable=False)

    songs = db.relationship("Songs", secondary=chords_songs_xref, back_populates="chords")

    def __init__(self, creator_id, chord_name, notes):
        self.creator_id = creator_id
        self.chord_name = chord_name
        self.notes = notes

    def get_new_chord(creator_id):
        return Chords(creator_id, "", "")


class ChordsSchema(ma.Schema):
    class Meta:
        fields = ["chord_id", "chord_name", "notes", "creator_id", "songs"]

    songs = ma.fields.Nested("SongsSchema", many=True, exclude=["chords"])


chord_schema = ChordsSchema()
chords_schema = ChordsSchema(many=True)
