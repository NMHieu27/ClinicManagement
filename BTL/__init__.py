from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary



app = Flask(__name__)
app.secret_key = 'DBW83972$^&*%$^&GH%&VHJKJJT&%$((0)'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/phongkhamdb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name = 'ddphodfop',
    api_key= '639657923925892',
    api_secret ='qUhE-fvxlzYeATpO5EtR5v6lG8M'
)


login = LoginManager(app=app)