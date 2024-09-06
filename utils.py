import json
from models import Vulnerability

def parse_burp_json(json_data):
    vulnerabilities = []
    for item in json_data.get('issues', []):
        vulnerabilities.append(Vulnerability(
            name=item.get('name'),
            severity=item.get('severity'),
            description=item.get('issueBackground'),
            remediation=item.get('remediationBackground'),
            reference=item.get('references')
        ))
    return vulnerabilities
