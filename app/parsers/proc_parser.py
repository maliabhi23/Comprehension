import re


def parse_proc(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        code = f.read()

    # PROC name
    proc_match = re.search(
        r"//([A-Z0-9#@$]+)\s+PROC",
        code,
        re.IGNORECASE
    )

    proc_name = (
        proc_match.group(1)
        if proc_match
        else "UNKNOWN"
    )

    # EXEC PGM
    exec_matches = re.findall(
        r"//([A-Z0-9#@$]+)\s+EXEC\s+PGM=([A-Z0-9#@$-]+)",
        code,
        re.IGNORECASE
    )

    steps = []

    for step, program in exec_matches:

        steps.append({
            "step": step,
            "program": program
        })

    return {
        "type": "proc",
        "proc_name": proc_name,
        "steps": steps
    }