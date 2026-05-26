from fastapi import FastAPI

from app.scanner.scanner import scan_repository

from app.parsers.cobol_parser import parse_cobol
from app.parsers.copybook_parser import parse_copybook
from app.parsers.jcl_parser import parse_jcl

from app.extractors.relation_extractor import build_relations

from app.ai.ollama_engine import generate_summary

app = FastAPI(title="Enterprise COBOL AI Parser")


@app.get("/analyze")
def analyze():

    repo_path = "sample_repo"
    # acces the repo and scan for files

    files = scan_repository(repo_path)

    parsed_results = []

    for file in files:
    # sending code to there parsers based on the file type and get the parsed results
        if file["type"] == "cobol":
            parsed_results.append(
                parse_cobol(file["path"])
            )

        elif file["type"] == "copybook":
            parsed_results.append(
                parse_copybook(file["path"])
            )

        elif file["type"] == "jcl":
            parsed_results.append(
                parse_jcl(file["path"])
            )

    relations = build_relations(parsed_results)

    summary = generate_summary(parsed_results[:5])

    return {
        "files_scanned": len(files),
        "parsed_results": parsed_results[:10],
        "relations": relations,
        "ai_summary": summary
    }