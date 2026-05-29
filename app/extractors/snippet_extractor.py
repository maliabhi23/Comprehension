import re


def clean_cobol_line(line):

    # Ignore very short lines
    if len(line) < 7:
        return None

    # Ignore COBOL comment lines
    if line[6] == "*":
        return None

    # Remove sequence numbers (columns 1-6)
    return line[6:]


def clean_cobol_code(code):

    cleaned = []

    for line in code.splitlines():

        cleaned_line = clean_cobol_line(line)

        if cleaned_line:
            cleaned.append(cleaned_line)

    return "\n".join(cleaned)


def extract_cobol_snippets(file_path):

    snippets = {
        "program_id": "",
        "working_storage": "",
        "procedure_division": "",
        "exec_sql_blocks": [],
        "paragraphs": [],
        "comments": []
    }

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            raw_code = f.read()

        # Clean COBOL fixed-format code
        code = clean_cobol_code(raw_code)

        # -----------------------------
        # PROGRAM-ID
        # -----------------------------
        program_match = re.search(
            r"PROGRAM-ID\.\s+([A-Z0-9-]+)",
            code,
            re.IGNORECASE
        )

        if program_match:

            snippets["program_id"] = (
                program_match.group(1)
            )

        # -----------------------------
        # WORKING-STORAGE SECTION
        # -----------------------------
        ws_match = re.search(
            r"WORKING-STORAGE SECTION\.(.*?)(PROCEDURE DIVISION\.)",
            code,
            re.IGNORECASE | re.DOTALL
        )

        if ws_match:

            snippets["working_storage"] = (
                ws_match.group(1).strip()[:3000]
            )

        # -----------------------------
        # PROCEDURE DIVISION
        # -----------------------------
        proc_match = re.search(
        r"PROCEDURE DIVISION.*?\.(.*)",
        code,
        re.IGNORECASE | re.DOTALL
        )

        if proc_match:

            snippets["procedure_division"] = (
                proc_match.group(1).strip()[:5000]
            )

        # -----------------------------
        # EXEC SQL BLOCKS
        # -----------------------------
        sql_blocks = re.findall(
            r"EXEC SQL(.*?)END-EXEC",
            code,
            re.IGNORECASE | re.DOTALL
        )

        snippets["exec_sql_blocks"] = [
            block.strip()[:1000]
            for block in sql_blocks
        ]

        # -----------------------------
        # Paragraph Names
        # -----------------------------
        paragraphs = re.findall(
            r"^\s{0,4}([A-Z0-9-]+)\.\s*$",
            code,
            re.MULTILINE
        )

        snippets["paragraphs"] = (
            paragraphs[:50]
        )

        # -----------------------------
        # Comments
        # -----------------------------
        comments = []

        for line in raw_code.splitlines():

            if len(line) > 6 and line[6] == "*":

                comments.append(
                    line[7:].strip()
                )

        snippets["comments"] = comments[:50]

    except Exception as e:

        snippets["error"] = str(e)

    return snippets