from flask import render_template


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.info("Route not found.")
        return render_template("404.html"), 404

    @app.errorhandler(429)
    def rate_limit_error(error):
        app.logger.warning("Rate limit exceeded.")
        return render_template("429.html"), 429

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception("Unhandled server error.")
        return render_template("500.html"), 500
