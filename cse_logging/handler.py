import uuid
import logging
from cse_logging.models import Log, db
from .__init__ import app
from sqlalchemy.sql import text


class PostgresHandler(logging.Handler):

    def __init__(self, service_name, autocommit=True):
        super().__init__()
        self.service_name = service_name
        self.autocommit = autocommit

    def emit(self, record):
        try:
            with app.app_context():
                trace_id = getattr(record, 'trace_id', str(uuid.uuid4()))
                user_id = getattr(record, 'user_id', None)
                log_type = getattr(record, 'log_type', 'application')
                context = getattr(record, 'context', {})
                module_name = getattr(record, 'module_name', '')

                log_entry = Log(
                    trace_id=trace_id,
                    user_id=user_id,
                    service_name=self.service_name,
                    module_name=module_name,
                    level=record.levelname,
                    log_type=log_type,
                    message=self.format(record),
                    context=context
                )

                db.session.add(log_entry)
                if self.autocommit:
                    db.session.commit()

        except Exception:
            self.handleError(record)


def init_logger(service_name: str, level=logging.INFO, autocommit=True) -> logging.Logger:
    logger = logging.getLogger(service_name)
    logger.setLevel(level)

    if not any(isinstance(h, PostgresHandler) for h in logger.handlers):
        handler = PostgresHandler(service_name, autocommit=autocommit)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def fetch_logs(filters, params, page, per_page):
    with app.app_context():
        offset = (page - 1) * per_page
        where_clause = "WHERE " + " AND ".join(filters) if filters else ""

        query = text(f"""
            SELECT * FROM logs
            {where_clause}
            ORDER BY timestamp DESC
            LIMIT :limit OFFSET :offset
        """)

        count_query = text(f"SELECT COUNT(*) FROM logs {where_clause}")

        params["limit"] = per_page
        params["offset"] = offset

        result = db.session.execute(query, params).mappings().all()
        total = db.session.execute(count_query, params).scalar()

        return result, total