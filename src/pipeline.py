import json

from src.extractor import ReferenceExtractor
from src.indexer import DocumentIndexer
from src.parser import DocumentParser
from src.resolver import ReferenceResolver

class Pipeline:

    def __init__(self):
        self.parser = DocumentParser()
        self.indexer = DocumentIndexer()
        self.extractor = ReferenceExtractor()
        self.resolver = ReferenceResolver()
    
    def parse_records(self, paragraphs: list[dict]) -> list[dict]:
        results = []

        for paragraph in paragraphs:
            text = paragraph.get("text", "")
            text_parsed = self.parser.run(text)
            text_parsed["id"] = paragraph.get("id", "")
            text_parsed["targetIds"] = paragraph.get("targetIds", [])
            results.append(text_parsed)
        
        return results
    
    def predict(self, data: dict) -> dict:
        paragraph_link = data.get("paragraphLinks", [])
        records = self.parse_records(paragraph_link)
        indexes = self.indexer.build_indices(records)

        output = []
        for item, record in zip(paragraph_link, records):
            refs = self.extractor.extract(record.get("body_text", ""))
            target_ids = self.resolver.resolve(refs, indexes)
            output.append({
                "text": item.get("text", ""),
                "id": item.get("id"),
                "targetIds": target_ids,
            })
        return {
            "documentVersionKey": data.get("documentVersionKey"),
            "documentVersionId": data.get("documentVersionId"),
            "rootRegion": data.get("rootRegion"),
            "region": data.get("region"),
            "paragraphLinks": output,
        }
    
def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
if __name__ == "__main__":
    input_path = "test_data.json"
    output_path = "data/test_predictions.json"

    data = load_json(input_path)
    pipeline = Pipeline()
    predictions = pipeline.predict(data)
    save_json(output_path, predictions)
    
