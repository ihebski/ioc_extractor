from app import app, db
from flask import render_template


@app.errorhandler(404)
def not_found(error):
    return render_template(
        'errors/404.html',
        title='Page Not Found',
        ), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template(
        'errors/500.html',
        title='Internal Server Error',
        ), 500


@app.errorhandler(400)
def bad_request(error):
    return render_template(
        'errors/400.html',
        title='Bad Request',
        ), 400


@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template(
        'errors/413.html',
        title='Request Entity Too Large',
        ), 413
