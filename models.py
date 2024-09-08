from app import db
from sqlalchemy import Enum
from sqlalchemy.ext.mutable import Mutable
import enum

# Define severity levels as an Enum for better validation and control
class SeverityLevel(enum.Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'

# Custom Mutable class to support JSON field updates in SQLAlchemy
class MutableList(Mutable, list):
    @staticmethod
    def coerce(key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                value = MutableList(value)
            else:
                value = MutableList()
        return value

class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    severity = db.Column(Enum(SeverityLevel), nullable=False)
    description = db.Column(db.Text, nullable=False)
    remediation = db.Column(db.Text, nullable=True)
    reference = db.Column(db.JSON, nullable=True)  # JSON field for flexible reference storage

    def __repr__(self):
        return f'<Vulnerability {self.name}>'
