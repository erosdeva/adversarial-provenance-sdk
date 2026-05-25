
import json
from datetime import datetime
from pathlib import Path

class AuditLogger:

    def __init__(self, path='audit.log'):
        self.path = Path(path)

    def log(self, payload: dict):
        with open(self.path, 'a') as f:
            f.write(json.dumps({
                'timestamp': datetime.utcnow().isoformat(),
                'payload': payload
            }) + '\n')
