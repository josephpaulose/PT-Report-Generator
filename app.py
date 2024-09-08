import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import or_
from flask_migrate import Migrate

# Initialize Flask-Migrate

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


# Database configuration from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Vulnerability model
class Vulnerability(db.Model):
    __tablename__ = 'cve_data'
    
    id = db.Column(db.Integer, primary_key=True)
    cve_id = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_published = db.Column(db.DateTime, nullable=True)
    references = db.Column(db.ARRAY(db.Text), nullable=True)  # Use ARRAY for PostgreSQL array type

    def __repr__(self):
        return f'<Vulnerability {self.cve_id}>'


# Serve the HTML file for the home page
@app.route('/')
def home():
    return render_template('index.html')

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

# Get all vulnerabilities or filter by CVE or search text with pagination
@app.route('/vulnerabilities', methods=['GET'])
def get_vulnerabilities():
    cve = request.args.get('cve')
    search_text = request.args.get('search')

    # Pagination parameters with defaults
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if cve:
        # Filter vulnerabilities by exact match of CVE ID in reference
        query = Vulnerability.query.filter(Vulnerability.cve_id.ilike(f'%{cve}%'))
    elif search_text:
        # Search for vulnerabilities where name or description contains the search text
        query = Vulnerability.query.filter(
            or_(
                Vulnerability.cve_id.ilike(f'%{search_text}%'),
                Vulnerability.description.ilike(f'%{search_text}%')
            )
        )
    else:
        query = Vulnerability.query

    # Debug: print the SQL query being executed
    print(query)

    # Apply pagination
    paginated_vulnerabilities = query.paginate(page=page, per_page=per_page, error_out=False)

    # Debug: Check if query returned any results
    print(f'Found vulnerabilities: {paginated_vulnerabilities.items}')

    output = []
    for vulnerability in paginated_vulnerabilities.items:
        output.append({
            'id': vulnerability.id,
            'cve_id': vulnerability.cve_id,
            'description': vulnerability.description,
            'date_published': vulnerability.date_published,
            'references': vulnerability.references
        })

    return jsonify({
        'vulnerabilities': output,
        'page': paginated_vulnerabilities.page,
        'per_page': paginated_vulnerabilities.per_page,
        'total_pages': paginated_vulnerabilities.pages,
        'total_vulnerabilities': paginated_vulnerabilities.total
    })



# Other routes (GET, PUT, DELETE vulnerabilities)...

if __name__ == '__main__':
    app.run(debug=True)
