from app.web import create_app

# Execute worker and complete celery setup
flask_app = create_app()
celery_app = flask_app.extensions["celery"]
