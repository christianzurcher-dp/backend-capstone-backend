from db import db


chords_songs_xref = db.Table(
    "ChordsSongsXref",
    db.Model.metadata,
    db.Column("chord_id", db.ForeignKey("Chords.chord_id"), primary_key=True),
    db.Column("song_id", db.ForeignKey("Songs.song_id"), primary_key=True)
)
