from app import app, db
from app.models import Track


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Track=Track)

db.create_all()
app.run(debug=True)
