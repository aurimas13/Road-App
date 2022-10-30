import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config_by_name


load_dotenv()
env = os.environ.get('APP_ENV')
app = Flask(__name__)
app.config.from_object(config_by_name[env])
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
