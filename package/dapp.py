from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow

from sqlalchemy import Date,Time,Integer,Float

from package import routes


dapp = Flask(__name__)

dapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
dapp.config['SQLALCHEMY_ECHO'] = True
dapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db =SQLAlchemy(dapp)

ma = Marshmallow(dapp)

class Observations(db.Model):
    """Defintion of the user model used by SQLAlchemy"""
    date  =db.Column(Date, primary_key=True)
    time = db.Column(Time, nullable=False)
    timezone_offset = db.Column(Integer, nullable=False)
    coordinates = db.Column(Float, nullable=False)
    temperature_land_surface = db.Column(Integer, nullable=False)
    temperature_sea_surface = db.Column(Integer, nullable=False)
    humidity = db.Column(Integer, nullable=False)
    wind_direction = db.Column(Integer, nullable=False)
    wind_speed = db.Column(Integer, nullable=False)
    precipitation= db.Column(Integer, nullable=False)
    haze = db.Column(Integer, nullable=False)

    
    def __repr__(self):
        return '<date %r>' % self.date
    
    class ObservationSchema(ma.SQLAlchemyAutoSchema):
        """defintion used by serialization library based on user model"""
        class Meta:
           fields = ("date","time"," timezone_offset","coordinates"," temperature_land_surface"," temperature_sea_surface",
                    "humidity "," wind_direction"," wind_speed "," precipitation"," haze")
           

    Observation_Schema = ObservationSchema()
    Observation_Schema = ObservationSchema(many=True)

    
@dapp.get("/")
def hello_world():
    return "hello world"

with dapp.app_context():
    db.create_all()

if __name__ == '__main__':
    dapp.run(debug=True)