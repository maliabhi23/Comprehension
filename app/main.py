from multiprocessing import context

from fastapi import FastAPI, HTTPException

from app.scanner.scanner import scan_repository

from app.parsers.cobol_parser import parse_cobol
from app.parsers.copybook_parser import parse_copybook
from app.parsers.jcl_parser import parse_jcl
from app.extractors.snippet_extractor import extract_cobol_snippets

from app.extractors.relation_extractor import build_relations

from app.ai.ollama_engine import generate_summary

from app.parsers.proc_parser import parse_proc
app = FastAPI(title="Enterprise COBOL AI Parser")


# -----------------------------
# Helper Function
# Context Retrieval Engine
# -----------------------------
def retrieve_related_context(program_name, parsed_results):

    related_context = []

    visited = set()

    def collect_program(program):

        if program in visited:
            return

        visited.add(program)

        for item in parsed_results:

            # ---------------------------------
            # COBOL PROGRAM
            # ---------------------------------
            if (
                item.get("type") == "cobol"
                and item.get("program") == program
            ):
                related_context.append(item)
                
                for copybook in item.get("copybooks", []):
                    for cp in parsed_results:
                        if (
                          cp.get("type") == "copybook"
                         and cp.get("copybook_name") == copybook
                  ):
                            related_context.append(cp)


                # Traverse called programs
                for called in item.get("calls", []):

                    collect_program(called)

            # ---------------------------------
            # JCL JOBS EXECUTING PROGRAM
            # ---------------------------------
            elif item.get("type") == "jcl":

                matched = False

                for step in item.get("steps", []):

                    if step.get("program") == program:

                        matched = True

                if matched:

                    related_context.append(item)

                    # Traverse PROC calls
                    for proc in item.get("procs", []):

                        collect_proc(
                            proc.get("proc")
                        )

    # ---------------------------------
    # PROC Traversal
    # ---------------------------------
    def collect_proc(proc_name):

        for item in parsed_results:

            if (
                item.get("type") == "proc"
                and item.get("proc_name") == proc_name
            ):

                related_context.append(item)

    collect_program(program_name)

    return related_context


# -----------------------------
# Full Repository Analysis
# -----------------------------
@app.get("/analyze")
def analyze():

    repo_path = "sample_repo"

    # Scan repository
    files = scan_repository(repo_path)

    parsed_results = []

    # Missing dependency tracking
    missing_copybooks = set()

    # Parse files
    for file in files:

        if file["type"] == "cobol":

            parsed_results.append(
                parse_cobol(file["path"])
            )

        elif file["type"] == "copybook":

            parsed_results.append(
                parse_copybook(file["path"])
            )
        elif file["type"] == "proc":
            parsed_results.append(
            parse_proc(file["path"])
            )

        elif file["type"] == "jcl":

            parsed_results.append(
                parse_jcl(file["path"])
            )

    # Build relations
    relations = build_relations(parsed_results)

    # Available copybooks
    available_copybooks = set()

    for file in files:

        if file["type"] == "copybook":

            filename = file["path"].split("\\")[-1]
            filename = filename.split(".")[0].upper()

            available_copybooks.add(filename)

    # Detect missing copybooks
    for item in parsed_results:

        if item.get("type") == "cobol":

            for copybook in item.get("copybooks", []):

                if copybook.upper() not in available_copybooks:

                    missing_copybooks.add(
                        copybook.upper()
                    )

    # Convert set to JSON format
    missing_copybooks = [
        {
            "copybook": copybook,
            "resolved": False
        }
        for copybook in sorted(missing_copybooks)
    ]

    return {
        "files_scanned": len(files),
        "parsed_results": parsed_results[:10],
        "relations": relations[:50],
        "missing_copybooks": missing_copybooks
    }


# -----------------------------
# Program Specific Comprehension
# Industry Style Context Retrieval
# -----------------------------
@app.get("/analyze/{program_name}")
def analyze_program(program_name: str):

    repo_path = "sample_repo"

    files = scan_repository(repo_path)

    parsed_results = []

    # Parse all files
    for file in files:

        if file["type"] == "cobol":

            parsed_results.append(
                parse_cobol(file["path"])
            )

        elif file["type"] == "copybook":

            parsed_results.append(
                parse_copybook(file["path"])
            )
        elif file["type"] == "proc":
            parsed_results.append(
                parse_proc(file["path"])
            )

        elif file["type"] == "jcl":

            parsed_results.append(
                parse_jcl(file["path"])
            )

    # Retrieve dependency-aware context
    context = retrieve_related_context(
    program_name.upper(),
    parsed_results
    )

    print("\n===== CONTEXT TYPES =====")

    for item in context:
        print(item.get("type"))

    print("=========================\n")

    snippet_context = []
    for file in files: 
        if file["type"] == "cobol":

            snippets = extract_cobol_snippets(
            file["path"]
            )

            if snippets.get("program_id") == program_name.upper():

               snippet_context.append(snippets)



    if not context:

        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    summary = generate_summary({
    "metadata": context,
    "snippets": snippet_context
    })

    return {
    "program": program_name,
    "context_size": len(context),
    "retrieved_context": context,
    "snippets": snippet_context,
    "ai_summary": summary
    }