import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.chords_songs_xref import chords_songs_xref


class Songs(db.Model):
    __tablename__ = "Songs"

    song_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    song_name = db.Column(db.String(), nullable=False)
    time_signature = db.Column(UUID(as_uuid=True), db.ForeignKey("TimeSignatures.time_signature_id"), nullable=False)

    chords = db.relationship("Chords", secondary=chords_songs_xref, back_populates="songs")

    def __init__(self, creator_id, song_name, time_signature):
        self.creator_id = creator_id
        self.song_name = song_name
        self.time_signature = time_signature

    def get_new_song(creator_id):
        return Songs(creator_id, "", "")


class SongsSchema(ma.Schema):
    class Meta:
        fields = ["song_id", "song_name", "time_signature", "creator_id", "chords"]

    chords = ma.fields.Nested("ChordsSchema", many=True, exclude=["songs"])


song_schema = SongsSchema()
songs_schema = SongsSchema(many=True)
