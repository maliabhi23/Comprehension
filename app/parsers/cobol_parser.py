import re


INVALID_COPYWORDS = {
    "OF",
    "REPLACING",
    "BY",
    "IN",
    "TO"
}


def clean_cobol_code(code):
    cleaned_lines = []

    for line in code.splitlines():

        # Ignore very short lines
        if len(line) < 7:
            continue

        # Ignore comment lines
        # Column 7 in COBOL fixed format
        if line[6] == "*":
            continue

        # Remove sequence numbers (columns 1-6)
        line = line[6:]

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def parse_cobol(file_path):

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_code = f.read()

    # Clean COBOL before parsing
    code = clean_cobol_code(raw_code)

    program_name = extract_program_name(code)

    # Better CALL parsing
    calls = re.findall(
        r"\bCALL\s+['\"]([A-Z0-9-]+)['\"]",
        code,
        re.IGNORECASE
    )

    # Better COPY parsing
    copybooks = re.findall(
        r"\bCOPY\s+([A-Z0-9-]+)",
        code,
        re.IGNORECASE
    )

    # Remove invalid words
    copybooks = [
        c for c in copybooks
        if c.upper() not in INVALID_COPYWORDS
    ]

    # File extraction
    files = re.findall(
        r"\bSELECT\s+([A-Z0-9-]+)",
        code,
        re.IGNORECASE
    )

    # SQL table extraction (only inside EXEC SQL blocks)
    sql_tables = []

    sql_blocks = re.findall(
        r"EXEC\s+SQL(.*?)END-EXEC",
        code,
        re.IGNORECASE | re.DOTALL
    )

    for block in sql_blocks:

        matches = re.findall(
            r"\bFROM\s+([A-Z0-9_.]+)",
            block,
            re.IGNORECASE
        )

        sql_tables.extend(matches)

    return {
        "type": "cobol",
        "program": program_name,
        "calls": sorted(list(set(calls))),
        "copybooks": sorted(list(set(copybooks))),
        "files": sorted(list(set(files))),
        "sql_tables": sorted(list(set(sql_tables)))
    }


def extract_program_name(code):

    match = re.search(
        r"PROGRAM-ID\.\s+([A-Z0-9-]+)",
        code,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return "UNKNOWN"