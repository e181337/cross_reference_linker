
class DocumentIndexer:
    def build_indices(self, records: list[dict]) -> dict:
        paragraph_index = {}
        annex_index = {}
        appendix_index = {}
        figure_index = {}

        for record in records:
            record_id = record.get("id")
            record_type = record.get("type")
            label = record.get("label")

            if not record_id or not label:
                continue

            if record_type == "paragraph":
                paragraph_index[label] = record_id

            elif record_type == "annex":
                annex_index[label] = record_id

            elif record_type == "appendix":
                appendix_index[label] = record_id

            elif record_type == "figure":
                figure_index[label] = record_id

        return {
            "paragraph_index": paragraph_index,
            "annex_index": annex_index,
            "appendix_index": appendix_index,
            "figure_index": figure_index,
        }
