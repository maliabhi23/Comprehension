import ollama


def generate_summary(parsed_data):
    prompt = f"""
You are an IBM Mainframe modernization expert.

Analyze the following mainframe metadata.

The application may contain:
- COBOL programs
- JCL jobs
- COPYBOOKS
- DB2 tables
- IMS segments
- MQ integrations
- Batch processing flows

Metadata:
{parsed_data}

Provide:
1. Program overview
2. Business functionality
3. Technical architecture
4. Dependencies
5. Database usage
6. Batch/JCL flow
7. Risks
8. Modernization recommendations

Do not hallucinate.
Only use information present in metadata.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]