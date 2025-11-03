from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from models import db
from flask_migrate import Migrate
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Use environment variables with safe defaults for local dev
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://youruser:yourpassword@localhost/meetingdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'change-me')
# Configure token expiry via environment (hours)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_EXP_HOURS', '1')))

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Register blueprints (auth, hr)
try:
	from blueprints.auth import auth_bp, hr_bp
	app.register_blueprint(auth_bp)
	app.register_blueprint(hr_bp)
except Exception:
	# Blueprint import/register will fail if packages are missing during initial setup
	pass


@app.route('/')
def index():
	return jsonify(status=200, message='Nexus API'), 200