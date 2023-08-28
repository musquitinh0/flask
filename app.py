from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import secrets

import urllib.parse as up
from db import DatabaseManager
#from config import get_uri


app = Flask(__name__)

url = up.urlparse('postgres://fguqqogd:EefId-spP1uZCdCtrn_CG94V-yVVMdxj@babar.db.elephantsql.com/fguqqogd')
up.uses_netloc.append("postgres")
default_port = '5432'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{url.username}:{url.password}@{url.hostname}:{default_port}/{url.path[1:]}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

secret_key = secrets.token_hex(32)
app.config['JWT_SECRET_KEY'] = secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)
CORS(app)

db = DatabaseManager.get_db()
db.init_app(app)

from routes import user_routes
from auth import auth_routes
app.register_blueprint(user_routes, url_prefix='/api')
app.register_blueprint(auth_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run()
    