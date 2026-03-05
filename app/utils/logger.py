import json
from datetime import datetime

LOG_FILE = "ai_logs.json"


def log_ai_interaction(module, prompt, response):

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "module": module,
        "prompt": prompt,
        "response": response,
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry, indent=2))
        f.write("\n\n")
