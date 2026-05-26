def build_relations(parsed_data):
    relations = []

    for item in parsed_data:
        if item.get("type") == "cobol":
            source = item.get("program")

            for called in item.get("calls", []):
                relations.append({
                    "source": source,
                    "target": called,
                    "relation": "CALLS"
                })

            for copybook in item.get("copybooks", []):
                relations.append({
                    "source": source,
                    "target": copybook,
                    "relation": "USES_COPYBOOK"
                })

    return relations