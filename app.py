import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Database configuration from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Vulnerability model
class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    remediation = db.Column(db.Text, nullable=True)
    reference = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Vulnerability {self.name}>'

# Define the home route
@app.route('/')
def home():
    return {"message": "Welcome to the VAPT Report Generator"}

# Create a vulnerability
@app.route('/vulnerabilities', methods=['POST'])
def create_vulnerability():
    data = request.json
    vulnerability = Vulnerability(
        name=data.get('name'),
        severity=data.get('severity'),
        description=data.get('description'),
        remediation=data.get('remediation'),
        reference=data.get('reference')
    )
    db.session.add(vulnerability)
    db.session.commit()
    return jsonify({"message": "Vulnerability created successfully"}), 201

# Get all vulnerabilities
@app.route('/vulnerabilities', methods=['GET'])
def get_vulnerabilities():
    vulnerabilities = Vulnerability.query.all()
    output = []
    for vulnerability in vulnerabilities:
        output.append({
            'id': vulnerability.id,
            'name': vulnerability.name,
            'severity': vulnerability.severity,
            'description': vulnerability.description,
            'remediation': vulnerability.remediation,
            'reference': vulnerability.reference
        })
    return jsonify(output)

# Get a vulnerability by ID
@app.route('/vulnerabilities/<int:id>', methods=['GET'])
def get_vulnerability(id):
    vulnerability = Vulnerability.query.get_or_404(id)
    return jsonify({
        'id': vulnerability.id,
        'name': vulnerability.name,
        'severity': vulnerability.severity,
        'description': vulnerability.description,
        'remediation': vulnerability.remediation,
        'reference': vulnerability.reference
    })

# Update a vulnerability
@app.route('/vulnerabilities/<int:id>', methods=['PUT'])
def update_vulnerability(id):
    vulnerability = Vulnerability.query.get_or_404(id)
    data = request.json
    vulnerability.name = data.get('name')
    vulnerability.severity = data.get('severity')
    vulnerability.description = data.get('description')
    vulnerability.remediation = data.get('remediation')
    vulnerability.reference = data.get('reference')
    db.session.commit()
    return jsonify({"message": "Vulnerability updated successfully"})

# Delete a vulnerability
@app.route('/vulnerabilities/<int:id>', methods=['DELETE'])
def delete_vulnerability(id):
    vulnerability = Vulnerability.query.get_or_404(id)
    db.session.delete(vulnerability)
    db.session.commit()
    return jsonify({"message": "Vulnerability deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
