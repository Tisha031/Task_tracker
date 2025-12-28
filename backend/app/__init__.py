from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, cors

def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get('FRONTEND_URL')}}, supports_credentials=True)

    # register blueprints
    from .routes.auth_routes import bp as auth_bp
    from .routes.category_routes import bp as category_bp
    from .routes.task_routes import bp as task_bp
    from .routes.admin_routes import bp as admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(task_bp, url_prefix="/api/tasks")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app
