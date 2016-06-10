from application import db
from sqlalchemy.orm import relationship

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    duration = db.Column(db.Integer)
    high_def = db.Column(db.Text)
    standard_def_small = db.Column(db.Text)
    standard_def_big = db.Column(db.Text)
    vimeo_id = db.Column(db.Integer)
    position = db.Column(db.Text)
    tags = relationship("Tag", secondary="video_tag")
    subtitle = relationship("Subtitle")
    short_name = db.Column(db.Text)

    def get_url(self, resolution="1280x720"):
        if resolution == "1280x720":
            return self.high_def
        elif resolution == "960x540":
            return self.standard_def_big
        else:
            return self.standard_def_small

    def json(self, resolution):
        return {'id': self.id,
                'name': self.name,
                'sub': self.subtitle[0].filename,
                'vid': self.vimeo_id,
                'short_name': self.short_name,
                'url': self.get_url(resolution)}

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text)
    videos = relationship("Video", secondary="video_tag")

class Subtitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.Text)
    filename = db.Column(db.Text)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))

video_tag = db.Table(
    'video_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('video_id', db.Integer, db.ForeignKey('video.id')),
    db.UniqueConstraint('tag_id', 'video_id')
)

db.create_all()
