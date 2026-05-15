def _patch_legacy_flask_imports():
    """Support old Flask packages in the local Anaconda environment."""
    try:
        import jinja2
        from markupsafe import escape, Markup
        if not hasattr(jinja2, "escape"):
            jinja2.escape = escape
        if not hasattr(jinja2, "Markup"):
            jinja2.Markup = Markup
    except Exception:
        pass

_patch_legacy_flask_imports()

from flask import Flask

from config import Config
from db.init_db import init_db
from routes.auth import bp as auth_bp
from routes.detection import bp as detection_bp
from routes.file import bp as file_bp
from routes.health import bp as health_bp
from routes.model import bp as model_bp
from utils.response import error_response


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    app.config["DATABASE"] = str(app.config.get("DATABASE"))
    app.config["STORAGE_ROOT"] = str(app.config.get("STORAGE_ROOT"))

    init_db(app)

    for bp in (health_bp, auth_bp, model_bp, detection_bp, file_bp):
        app.register_blueprint(bp, url_prefix=Config.API_PREFIX)

    @app.after_request
    def add_cors_headers(response):
        response.headers.setdefault("Access-Control-Allow-Origin", "*")
        response.headers.setdefault("Access-Control-Allow-Headers", "Authorization, Content-Type")
        response.headers.setdefault("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        return response

    @app.errorhandler(404)
    def handle_not_found(_exc):
        return error_response("not found", code=404, http_status=404)

    @app.errorhandler(413)
    def handle_too_large(_exc):
        return error_response("file too large", code=400, http_status=400)

    @app.errorhandler(Exception)
    def handle_unexpected(exc):
        app.logger.exception("Unhandled error: %s", exc)
        return error_response("internal server error", code=500, http_status=500)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
