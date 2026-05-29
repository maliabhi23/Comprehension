def build_relations(parsed_data):

    relations = []

    for item in parsed_data:

        # ---------------------------------
        # COBOL Relations
        # ---------------------------------
        if item.get("type") == "cobol":

            source = item.get("program")

            # PROGRAM -> PROGRAM
            for called in item.get("calls", []):

                relations.append({
                    "source": source,
                    "target": called,
                    "relation": "CALLS"
                })

            # PROGRAM -> COPYBOOK
            for copybook in item.get("copybooks", []):

                relations.append({
                    "source": source,
                    "target": copybook,
                    "relation": "USES_COPYBOOK"
                })

            # PROGRAM -> SQL TABLE
            for table in item.get("sql_tables", []):

                relations.append({
                    "source": source,
                    "target": table,
                    "relation": "USES_SQL_TABLE"
                })

            # PROGRAM -> FILE
            for file_name in item.get("files", []):

                relations.append({
                    "source": source,
                    "target": file_name,
                    "relation": "USES_FILE"
                })

        # ---------------------------------
        # JCL Relations
        # ---------------------------------
        elif item.get("type") == "jcl":

            source = item.get("job_name")

            # JOB -> PROGRAM
            for step in item.get("steps", []):

                relations.append({
                    "source": source,
                    "target": step["program"],
                    "relation": "EXECUTES_PROGRAM"
                })

            # JOB -> PROC
            for proc in item.get("procs", []):

                relations.append({
                    "source": source,
                    "target": proc["proc"],
                    "relation": "USES_PROC"
                })

            # JOB -> DATASET
            for dataset in item.get("datasets", []):

                relations.append({
                    "source": source,
                    "target": dataset,
                    "relation": "USES_DATASET"
                })

    return relations