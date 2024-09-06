from app import db

class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    remediation = db.Column(db.Text, nullable=True)
    reference = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Vulnerability {self.name}>'
