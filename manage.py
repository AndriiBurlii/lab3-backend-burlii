
from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

# Enables: flask --app manage.py db init/migrate/upgrade
