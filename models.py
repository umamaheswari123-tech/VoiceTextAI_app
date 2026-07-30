from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TranscriptionHistory(db.Model):
    __tablename__ = 'transcription_history'
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(200))
    transcribed_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.original_filename,
            'text': self.transcribed_text,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class SpeechHistory(db.Model):
    __tablename__ = 'speech_history'
    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text)
    language = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.input_text,
            'language': self.language,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }