import os

COBOL_EXTENSIONS = (".cbl", ".cob", ".cobol")
COPYBOOK_EXTENSIONS = (".cpy",)
JCL_EXTENSIONS = (".jcl",)


def scan_repository(repo_path):
    files = []

    for root, dirs, filenames in os.walk(repo_path):
        for filename in filenames:
            path = os.path.join(root, filename)

            if filename.lower().endswith(COBOL_EXTENSIONS):
                files.append({
                    "type": "cobol",
                    "path": path
                })

            elif filename.lower().endswith(COPYBOOK_EXTENSIONS):
                files.append({
                    "type": "copybook",
                    "path": path
                })

            elif filename.lower().endswith(JCL_EXTENSIONS):
                files.append({
                    "type": "jcl",
                    "path": path
                })

    return files