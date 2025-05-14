from flask import Flask
# from cse_logging.models import db
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sparkai123@localhost/test-db'

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()
