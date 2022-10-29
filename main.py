from app import app, db
from app.models import Weather, Traffic, BatchUpdate


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Weather': Weather, 'Traffic': Traffic, 'BatchUpdate': BatchUpdate}

