import json
from datetime import datetime
from pathlib import Path

LOG_FILE = "ai_logs.json"


def log_ai_interaction(module: str, prompt: str, response: str) -> None:
    """
    Append an AI interaction log entry to ai_logs.json.
    Maintains a valid JSON array so the file can always be parsed.
    """
    path = Path(LOG_FILE)

    # load existing logs or start fresh
    if path.exists() and path.stat().st_size > 0:
        try:
            logs = json.loads(path.read_text())
        except json.JSONDecodeError:
            logs = []
    else:
        logs = []

    logs.append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "module": module,
            "prompt": prompt,
            "response": response,
        }
    )

    path.write_text(json.dumps(logs, indent=2))
