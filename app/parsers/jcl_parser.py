import re


def parse_jcl(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    jobs = re.findall(
        r"//([A-Z0-9]+)\s+JOB",
        code,
        re.IGNORECASE
    )

    programs = re.findall(
        r"EXEC\s+PGM=([A-Z0-9-]+)",
        code,
        re.IGNORECASE
    )

    return {
        "type": "jcl",
        "jobs": jobs,
        "programs": programs
    }