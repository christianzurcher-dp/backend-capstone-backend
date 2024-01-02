import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class TimeSignatures(db.Model):
    __tablename__ = "TimeSignatures"

    time_signature_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    time_signature_name = db.Column(db.String(), nullable=False)
    metre = db.Column(db.String(), nullable=False)
    chord_timing = db.Column(db.String(), nullable=False)

    def __init__(self, creator_id, time_signature_name, metre, chord_timing):
        self.creator_id = creator_id
        self.time_signature_name = time_signature_name
        self.metre = metre
        self.chord_timing = chord_timing

    def get_new_time_signature(creator_id):
        return TimeSignatures(creator_id, "", "", "")


class TimeSignaturesSchema(ma.Schema):
    class Meta:
        fields = ["time_signature_id", "time_signature_name", "metre", "chord_timing", "creator_id"]


time_signature_schema = TimeSignaturesSchema()
time_signatures_schema = TimeSignaturesSchema(many=True)
