import ollama


def generate_summary(parsed_data):

    prompt = f"""
You are an IBM Mainframe Application Comprehension expert.

Analyze ONLY the provided mainframe metadata, retrieved dependency context, and extracted COBOL/JCL snippets.

STRICT RULES:
- Use ONLY information explicitly present in the context.
- NEVER assume DB2, IMS, MQ, JCL, Batch processing, or business functionality unless explicitly visible.
- If information is missing, clearly say:
  "Not enough contextual information available."
- Do NOT invent architecture details.
- Do NOT generate generic modernization advice.
- Keep the response factual, grounded, and enterprise-focused.

Context:
{parsed_data}

Generate the following sections:

1. Program Overview
- Mention detected programs only.
- Mention detected technologies only if present.

2. Technical Summary
- Explain detected CALL dependencies.
- Explain detected COPYBOOK usage.
- Mention detected file references.
- Mention detected SQL usage only if sql_tables exist.

3. Dependency Analysis
- Mention program relationships only if present.
- Mention unresolved/missing dependencies if visible.

4. Database Analysis
- Mention SQL tables ONLY if detected.
- If no SQL metadata exists, say:
  "No SQL metadata detected."

5. Risk Assessment
- Mention risks ONLY based on available metadata.
- Example:
  - unresolved dependencies
  - missing copybooks
  - limited visibility
  - legacy complexity

6. Modernization Recommendations
- Give modernization suggestions ONLY based on detected metadata.
- Avoid generic cloud/container recommendations unless relevant.

7. Confidence Assessment
- Mention whether comprehension confidence is:
  - HIGH
  - MEDIUM
  - LOW

Rules:
- Mention MQ ONLY if MQ calls exist.
- Mention IMS ONLY if IMS calls exist.
- Mention batch/JCL ONLY if JCL metadata exists.
- Mention business functionality ONLY if procedure logic/comments exist.
- If PROCEDURE DIVISION is empty, say:
  "Business logic not available."

If metadata is limited, clearly state:
"Comprehension confidence is LOW due to insufficient contextual metadata."

Return a professional enterprise-style technical comprehension report.
"""
    print("========== LLM INPUT ==========")
    print(prompt)
    print("================================")
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return (
        response["message"]["content"]
        .replace("\\t", " ")
        .replace("\t", " ")
        .replace("\\n", "\n")
    )