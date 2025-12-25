import logging
from logging import config as logging_config
from uuid import uuid4

from flask import g, has_request_context, request


class RequestContextFilter(logging.Filter):
    def filter(self, record):
        if has_request_context():
            record.request_id = getattr(g, "request_id", "-")
            record.method = request.method
            record.path = request.path
            record.remote_addr = request.headers.get("X-Forwarded-For", request.remote_addr)
        else:
            record.request_id = "-"
            record.method = "-"
            record.path = "-"
            record.remote_addr = "-"
        return True


def configure_logging(app):
    log_level = app.config.get("LOG_LEVEL", "INFO")
    logging_config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {"request_context": {"()": RequestContextFilter}},
            "formatters": {
                "default": {
                    "format": (
                        "%(asctime)s %(levelname)s %(name)s "
                        "request_id=%(request_id)s method=%(method)s path=%(path)s "
                        "remote_addr=%(remote_addr)s message=%(message)s"
                    )
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "filters": ["request_context"],
                }
            },
            "root": {"handlers": ["console"], "level": log_level},
        }
    )
    app.logger.propagate = True


def init_request_context(app):
    @app.before_request
    def assign_request_id():
        g.request_id = uuid4().hex

    @app.after_request
    def attach_request_id(response):
        response.headers["X-Request-ID"] = getattr(g, "request_id", "-")
        return response
