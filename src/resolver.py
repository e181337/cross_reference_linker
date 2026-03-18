import re

class ReferenceResolver:

    def normalize(self, texts: str) -> list[str]:

        if not texts:
            return []
        
        # split "and" and ","
        pattern = r"\s*(?:and|,)\s*"

        text = re.split(pattern, texts, flags=re.IGNORECASE)

        paragraph_result = []
        for value in text:
            value = value.strip()
            value = value.rstrip(".")
            if value:
                paragraph_result.append(value)

        return paragraph_result
    
    def resolve(self, references: list[dict], indexes: dict) -> list[str]:

        target_values = []

        paragraph_index = indexes.get("paragraph_index", {})
        annex_index = indexes.get("annex_index", {})
        appendix_index = indexes.get("appendix_index", {})
        figure_index = indexes.get("figure_index", {})

        for reference in references:
            reference_type = reference.get("type")
            value = reference.get("value")

                        
            if reference_type == "paragraph":
                values = self.normalize(value)
                for item in values:
                    id = paragraph_index.get(item)
                    if id:
                        target_values.append(id)

            elif reference_type == "annex":
                id = annex_index.get(value)
                if id:
                    target_values.append(id)

            elif reference_type == "appendix":
                id = appendix_index.get(value)
                if id:
                    target_values.append(id)

            elif reference_type == "figure":
                id = figure_index.get(value)
                if id:
                    target_values.append(id)    
            
        seen = set()
        result = []

        for item in target_values:
            if item not in seen:
                seen.add(item)
                result.append(item)

        return result

        
