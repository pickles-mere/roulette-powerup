import json
import csv
from datetime import datetime
from pathlib import Path

class HistoryLog:
    def __init__(self, json_path="history.json", csv_path="history.csv", append=True):
        self.json_path = Path(json_path)
        self.csv_path = Path(csv_path)
        self.fields = None
        if not append:
            if self.json_path.exists(): self.json_path.unlink()
            if self.csv_path.exists(): self.csv_path.unlink()

    def append(self, event: dict):
        """Append an event dict to JSON (newline-delimited) and CSV."""
        if 'timestamp' not in event:
            event['timestamp'] = datetime.utcnow().isoformat()

        with open(self.json_path, "a", encoding="utf-8") as jf:
            jf.write(json.dumps(event) + "\n")

        if self.fields is None:
            self.fields = list(event.keys())
            write_header = not self.csv_path.exists()
            with open(self.csv_path, "a", newline='', encoding="utf-8") as cf:
                writer = csv.DictWriter(cf, fieldnames=self.fields)
                if write_header:
                    writer.writeheader()
                writer.writerow(event)
        else:
            with open(self.csv_path, "a", newline='', encoding="utf-8") as cf:
                writer = csv.DictWriter(cf, fieldnames=self.fields)
                row = {k: event.get(k, "") for k in self.fields}
                writer.writerow(row)

    def read_json_lines(self):
        """Read back json lines into a list of dicts (if file exists)."""
        events = []
        if self.json_path.exists():
            with open(self.json_path, "r", encoding="utf-8") as jf:
                for line in jf:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        events.append(json.loads(line))
                    except Exception:
                        continue
        return events
