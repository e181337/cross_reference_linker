import re

class ReferenceExtractor:
    def extract(self, text: str) -> list[dict]:
        if not text:
            return []

        refs = []

        # paragraph
        pattern = r"\bparagraphs?\s+(\d+(?:\.\d+)*\.?(?:\s*(?:,|and|to)\s*\d+(?:\.\d+)*\.?)*)"
        
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            
            raw = match.group(0)
            value = match.group(1)
            refs.append({
                    "type": "paragraph",
                    "raw": raw,
                    "value": value,
                })
        
        # annex
        pattern = r"\b(Annex\s+\d+)\b"

        for match in re.finditer(pattern, text, flags=re.IGNORECASE):

            raw = match.group(0)
            value = match.group(1)
            refs.append({
                    "type": "annex",
                    "raw": raw,
                    "value": value,
                })
        
        # appendix of annex
        pattern = r"\b(Appendix\s+\d+\s+(?:of|to)\s+Annex\s+\d+)\b"

        for match in re.finditer(pattern, text, flags=re.IGNORECASE):

            raw = match.group(0)
            value = match.group(1)
            refs.append({
                    "type": "appendix",
                    "raw": raw,
                    "value": value,
                })

        # figure
        pattern = r"\b(Figure\s+\d+)\b"
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):

            raw = match.group(0)
            value = match.group(1)
            refs.append({
                    "type": "figure",
                    "raw": raw,
                    "value": value,
                })

        return refs

