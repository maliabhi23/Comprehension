import re


def parse_copybook(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    fields = re.findall(
        r"\d+\s+([A-Z0-9-]+)\s+PIC",
        code,
        re.IGNORECASE
    )

    return {
        "type": "copybook",
        "fields": fields
    }