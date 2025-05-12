import uuid
import logging
from datetime import datetime, timezone
from .models import Log, db


class PostgresHandler(logging.Handler):

    def __init__(self, service_name, autocommit=True):
        super().__init__()
        self.service_name = service_name
        self.autocommit = autocommit

    def emit(self, record):
        try:
            trace_id = getattr(record, 'trace_id', str(uuid.uuid4()))
            user_id = getattr(record, 'user_id', None)
            log_type = getattr(record, 'log_type', 'application')
            context = getattr(record, 'context', {})

            log_entry = Log(
                trace_id=trace_id,
                timestamp=datetime.now(timezone.utc),
                user_id=user_id,
                service_name=self.service_name,
                module_name=record.funcName,
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
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
