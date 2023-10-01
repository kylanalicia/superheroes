from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    super_name = db.Column(db.String(255),nullable=False)
    powers = db.relationship('HeroPower',back_popukates='hero',overlaps='hero')

# add any models you may need. 