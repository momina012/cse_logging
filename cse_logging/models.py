from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timezone

db = SQLAlchemy()

class Log(db.Model):
    __tablename__ = 'logs'

    trace_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), nullable=True)
    service_name = db.Column(db.String(100), nullable=False)
    module_name = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    log_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    context = db.Column(JSONB, nullable=True)