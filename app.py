from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User  # Importe tes modèles
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'  # Remplace par tes creds (ou via env pour Docker)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change ça en prod !

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Tes routes vont ici (voir ci-dessous)