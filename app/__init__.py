from flask import Flask

from app import routes
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(routes.bp)
