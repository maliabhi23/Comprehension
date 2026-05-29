# Enterprise COBOL AI Comprehension Engine

## 1. Introduction

### 1.1 Program Overview

This project is an AI-assisted Mainframe Application Comprehension and Dependency Analysis Engine designed for enterprise COBOL modernization initiatives.

The system scans legacy mainframe repositories, parses COBOL/JCL/COPYBOOK files, extracts metadata and dependency relationships, and generates AI-powered comprehension summaries using locally hosted LLMs through Ollama.

The solution focuses on:
- Legacy application understanding
- Dependency discovery
- Mainframe modernization analysis
- Technical comprehension generation
- Metadata-driven AI summarization

The implementation uses FastAPI for REST APIs and locally executed LLMs for secure offline processing.

---

### 1.2 Objectives

The primary objectives of this project are:

- Parse enterprise COBOL repositories
- Extract program metadata
- Detect COPYBOOK dependencies
- Identify inter-program CALL relationships
- Detect DB2 SQL usage
- Build dependency relations
- Generate AI-powered technical comprehension
- Support modernization assessment activities
- Reduce manual analysis effort for legacy systems

---

### 1.3 Scope

The current implementation supports:

- COBOL parsing
- COPYBOOK parsing
- JCL parsing
- Repository scanning
- Dependency graph generation
- Metadata extraction
- AI comprehension generation using Ollama
- Basic DB2 SQL extraction
- REST API-based execution

The project currently focuses on static analysis and metadata-driven comprehension generation.

---

### 1.4 Assumptions and Constraints

#### Assumptions

- COBOL repositories are accessible locally
- Standard COBOL syntax is used
- Local Ollama runtime is available
- Input repositories contain parsable COBOL/JCL/COPYBOOK files

#### Constraints

- Current implementation uses regex-based parsing
- Dynamic runtime execution analysis is not implemented
- Some external COPYBOOK libraries may not be available
- Complex COBOL dialects may require advanced parsing support
- Dependency analysis is based on static source inspection

---

# 2. Database Details

## 2.1 DB2 Tables

The system detects DB2 SQL usage by analyzing:

```cobol
EXEC SQL
...
END-EXEC

```
blocks within COBOL programs.

Example extracted DB2 table:

```
SYSIBM.SYSDUMMY1
```
DB2 metadata extraction currently supports:

SELECT statements
FROM clause parsing
Basic table reference extraction

2.2 IMS Segments

The parser partially supports IMS-related metadata extraction.

IMS interactions are identified using IMS-specific calls such as:

```
CBLTDLI
```
These calls indicate IMS transaction/database interaction within COBOL programs.

2.3 IDMS Records

IDMS-specific parsing is not implemented in the current version.

Future enhancement scope includes:

IDMS schema parsing
Record extraction
IDMS dependency analysis

3.System Architecture
3.1 Component Diagram

The system architecture contains the following components:

---
| Component          | Responsibility                 |
| ------------------ | ------------------------------ |
| Repository Scanner | Scans repositories recursively |
| COBOL Parser       | Extracts COBOL metadata        |
| COPYBOOK Parser    | Detects shared structure usage |
| JCL Parser         | Extracts batch job information |
| Relation Extractor | Builds dependency relations    |
| Ollama Engine      | Generates AI comprehension     |
| FastAPI Service    | Exposes REST APIs              |

---

High-Level Flow

```
Mainframe Repository
        ↓
Repository Scanner
        ↓
COBOL/JCL/COPYBOOK Parsers
        ↓
Metadata Extraction
        ↓
Relation Builder
        ↓
AI Comprehension Engine
        ↓
REST API Response

```
3.2 Control Flow Diagram
Processing Flow
```
Repository Scan
      ↓
File Type Detection
      ↓
COBOL / JCL / COPYBOOK Parsing
      ↓
Metadata Extraction
      ↓
Dependency Relation Generation
      ↓
AI Prompt Construction
      ↓
Ollama-Based Comprehension Generation
      ↓
API Response Generation
```
4. Detailed Design
4.1 Program Structure

The project follows a modular architecture.

Main Modules

---
| Module     | Description                |
| ---------- | -------------------------- |
| scanner    | Repository scanning        |
| parsers    | COBOL/JCL/COPYBOOK parsing |
| extractors | Relation extraction        |
| ai         | Ollama integration         |
| main.py    | FastAPI entry point        |
---

COBOL Metadata Extracted

The parser extracts:

PROGRAM-ID
CALL statements
COPYBOOK references
File references
DB2 SQL tables

Example parsed metadata:

```
{
  "program": "COPAUA0C",
  "calls": ["MQOPEN", "MQGET"],
  "copybooks": ["CIPAUDTY"],
  "sql_tables": ["SYSIBM.SYSDUMMY1"]
}
```
4.2 Algorithms
```
Repository Scanning Algorithm
```

```
1.Traverse repository recursively
2.Identify file types using extensions
3.Categorize:
COBOL
COPYBOOK
JCL
4.Send files to appropriate parsers
```
```

COBOL Parsing Algorithm
1.Read COBOL source file
2.Preprocess fixed-format COBOL
3.Remove sequence numbers
4.Ignore comment lines
5.Extract:
PROGRAM-ID
CALL statements
COPY statements
EXEC SQL blocks
6.Generate structured metadata

```

Relation Extraction Algorithm

Relations are generated using extracted metadata.

Examples:

PROGRAM → CALLS → PROGRAM
PROGRAM → USES_COPYBOOK → COPYBOOK

Example:

```
{
  "source": "COPAUA0C",
  "target": "MQOPEN",
  "relation": "CALLS"
}
```
AI Comprehension Generation

The comprehension engine uses:

Ollama
llama3.2:3b

Metadata is provided to the LLM for:

business understanding
technical summarization
dependency explanation
modernization analysis

The implementation follows a metadata-grounded AI approach to reduce hallucinations.

4.3 Input/Output Specifications
Input

Input repository may contain:

.cbl
.cob
.cobol
.cpy
.jcl

Example input:
```
sample_repo/
```
Output

The API returns:

parsed metadata
dependency relations
AI-generated comprehension summaries

Example output:

```
{
  "files_scanned": 161,
  "parsed_results": [
    {
      "program": "COPAUA0C",
      "calls": ["MQOPEN"],
      "copybooks": ["CIPAUDTY"]
    }
  ]
}
```
Validation and Accuracy Considerations

To reduce hallucinations and improve trustworthiness:

AI summaries are generated only from extracted metadata
Fixed-format COBOL preprocessing is implemented
SQL extraction is limited to EXEC SQL blocks
Comment filtering is implemented
Dependency extraction is grounded in static analysis

The project prioritizes metadata-driven comprehension instead of unrestricted LLM generation.

---
| Technology    | Purpose                    |
| ------------- | -------------------------- |
| Python        | Core implementation        |
| FastAPI       | REST APIs                  |
| Ollama        | Local LLM runtime          |
| llama3.2:3b   | AI comprehension           |
| Regex Parsing | Static metadata extraction |

---

Current Limitations
Regex-based parsing has limited semantic understanding
Full AST parsing is not implemented
Some COPYBOOK files may exist externally
Runtime execution flow analysis is not implemented
Advanced IMS/IDMS parsing is pending
Future Enhancements

Planned enhancements include:

AST-based COBOL parsing
Neo4j graph integration
Semantic search using embeddings
Impact analysis engine
Architecture visualization
Copybook resolution engine
Enhanced DB2 parsing
Control flow analysis
IMS/IDMS deep parsing

API Usage
Run FastAPI

```
uvicorn app.main:app --reload
```
Swagger Documentation
```
http://127.0.0.1:8000/docs
```

Analyze Endpoint
```
GET /analyze
```

Conclusion

This project demonstrates an enterprise-aligned approach for AI-assisted mainframe comprehension and dependency analysis.

The system helps organizations understand legacy COBOL applications using metadata-driven AI summarization and dependency extraction techniques, supporting modernization and migration assessment initiatives.-