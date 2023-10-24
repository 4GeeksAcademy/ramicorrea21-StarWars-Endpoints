from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Characters(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    gender = db.Column(db.String(10), nullable=False, unique=False)
    is_alive = db.Column(db.Boolean(), nullable=False, unique=False)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "is_alive": self.is_alive
        }

class Planets(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    climate = db.Column(db.String(10), nullable=False, unique=False)
    population = db.Column(db.Integer(), nullable=False, unique=False)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population
        }