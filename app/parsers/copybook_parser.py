import re
import os


def parse_copybook(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        code = f.read()

    fields = re.findall(
        r"\d+\s+([A-Z0-9-]+)\s+PIC",
        code,
        re.IGNORECASE
    )

    return {
        "type": "copybook",
        "copybook_name": os.path.splitext(
            os.path.basename(file_path)
        )[0].upper(),
        "fields": fields
    }