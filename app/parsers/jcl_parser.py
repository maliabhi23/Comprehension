import re


def parse_jcl(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        code = f.read()

    # -----------------------------
    # JOB NAME
    # -----------------------------
    job_match = re.search(
        r"//([A-Z0-9#@$]+)\s+JOB",
        code,
        re.IGNORECASE
    )

    job_name = (
        job_match.group(1)
        if job_match
        else "UNKNOWN"
    )

    # -----------------------------
    # STEP + EXEC PGM
    # -----------------------------
    steps = []

    exec_matches = re.findall(
        r"//([A-Z0-9#@$]+)\s+EXEC\s+PGM=([A-Z0-9#@$-]+)",
        code,
        re.IGNORECASE
    )

    for step, program in exec_matches:

        steps.append({
            "step": step,
            "program": program
        })

    # -----------------------------
    # PROC CALLS
    # -----------------------------
    proc_matches = re.findall(
        r"//([A-Z0-9#@$]+)\s+EXEC\s+PROC=([A-Z0-9#@$-]+)",
        code,
        re.IGNORECASE
    )

    procs = []

    for step, proc in proc_matches:

        procs.append({
            "step": step,
            "proc": proc
        })

    # -----------------------------
    # DATASETS (DSN=)
    # -----------------------------
    datasets = re.findall(
        r"DSN=([A-Z0-9.#@$-]+)",
        code,
        re.IGNORECASE
    )

    # -----------------------------
    # DD Statements
    # -----------------------------
    ddnames = re.findall(
        r"//([A-Z0-9#@$]+)\s+DD",
        code,
        re.IGNORECASE
    )

    # -----------------------------
    # SYSIN Detection
    # -----------------------------
    sysin_present = bool(
        re.search(
            r"//SYSIN\s+DD",
            code,
            re.IGNORECASE
        )
    )

    return {
        "type": "jcl",
        "job_name": job_name,
        "steps": steps,
        "procs": procs,
        "datasets": sorted(list(set(datasets))),
        "dd_statements": sorted(list(set(ddnames))),
        "sysin_present": sysin_present
    }